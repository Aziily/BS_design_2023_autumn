from pydoc import cli
import random
from re import sub
import time
from paho.mqtt import client as mqtt_client
import pymysql
import atexit
import os

from omegaconf import OmegaConf
conf = OmegaConf.load("config.yaml")

broker = 'broker.emqx.io'
port = 1883
interval = 5
client = mqtt_client.Client("bs")

class device:
    def __init__(self, did, uid, name, description, type, status, ip):
        self.did = did
        self.uid = uid
        self.name = name
        self.description = description
        self.type = type
        self.status = status
        self.ip = ip
class sensorData:
    def __init__(self, sdid, did, level, message, timestamp, data):
        self.template = 'level: {0}, message: {1}, timestamp: {2}, data: {3}'
        
        self.sdid = sdid
        self.did = did
        self.level = level
        self.message = message
        self.timestamp = timestamp
        self.data = data
class actuatorData:
    def __init__(self, adid, did, level, message, timestamp, data):
        self.template = 'level: {0}, message: {1}, timestamp: {2}, data: {3}'
        
        self.adid = adid
        self.did = did
        self.level = level
        self.message = message
        self.timestamp = timestamp
        self.data = data

broker = 'broker.emqx.io'
port = 1883
# generate client ID with pub prefix randomly
client_id = 'bs_sub'
devices_map = {}
conn = pymysql.connect(host=conf.database.ip, port=int(conf.database.port), user=conf.database.user, password=conf.database.password, db=conf.database.database)
cursor = conn.cursor()

def checkConn():
    global conn, cursor
    try:
        conn.ping()
    except:
        conn = pymysql.connect(host=conf.database.ip, port=int(conf.database.port), user=conf.database.user, password=conf.database.password, db=conf.database.database)
        cursor = conn.cursor()

def getDeviceList():
    checkConn()
    cursor.execute("SELECT * FROM device")
    deviceList = []
    for row in cursor.fetchall():
        deviceList.append(device(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))    
    return deviceList

def connect_mqtt() -> mqtt_client.Client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client.Client):
    devices = {}
    devices_map = {}
    for device in getDeviceList():
        typename = "sensor" if device.type == 0 else "actuator"
        if device.status == 1:
            devices[device.did] = typename + "/" + str(device.ip)
            devices_map[devices[device.did]] = device.did
    for device in devices:
        client.subscribe(devices[device])
    return devices_map

def unsubscribe(client: mqtt_client.Client):
    for device in getDeviceList():
        typename = "sensor" if device.type == 0 else "actuator"
        client.unsubscribe(typename + "/" + str(device.ip))

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    # print(devices_map)
    did = devices_map[msg.topic]
    if 'sensor' in msg.topic:
        msg_payload = msg.payload.decode()
        msg_payload = sub('level: ', '', msg_payload)
        msg_payload = sub('message: ', '', msg_payload)
        msg_payload = sub('timestamp: ', '', msg_payload)
        msg_payload = sub('data: ', '', msg_payload)
        msg_payload = msg_payload.split(', ')
        level = int(msg_payload[0])
        message = msg_payload[1]
        timestamp = int(float(msg_payload[2]))
        data = float(msg_payload[3])
    elif 'actuator' in msg.topic:
        msg_payload = msg.payload.decode()
        msg_payload = sub('level: ', '', msg_payload)
        msg_payload = sub('message: ', '', msg_payload)
        msg_payload = sub('timestamp: ', '', msg_payload)
        msg_payload = sub('data: ', '', msg_payload)
        msg_payload = msg_payload.split(', ')
        level = int(msg_payload[0])
        message = msg_payload[1]
        timestamp = int(float(msg_payload[2]))
        data = int(msg_payload[3])
    else:
        return
    checkConn()
    table = "sensor_data" if 'sensor' in msg.topic else "actuator_data"
    cursor.execute("INSERT INTO " + table + " (did, level, message, timestamp, data) VALUES (%s, %s, %s, %s, %s)", (did, level, message, timestamp, data))
    conn.commit()

def run():
    client = connect_mqtt()
    client.on_message = on_message
    
    client.loop_start()

    while True:
        global devices_map
        devices_map = subscribe(client)
        time.sleep(interval)
        # print("sleep")
        unsubscribe(client)

def defer():
    print("defer")
    unsubscribe(client)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    atexit.register(defer)
    run()