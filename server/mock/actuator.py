from email import message
import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
typename = "actuator"
ip = "192.168.255.255"
client = mqtt_client.Client("bs")
client.connect(broker, port)
client.loop_start()

while True:
    time.sleep(5)
    message_template = 'level: {0}, message: {1}, timestamp: {2}, data: {3}'
    level = 0 if random.random() < 0.95 else 1
    message = message_template.format(level, "test", time.time(), random.randint(0, 1))
    client.publish(typename + "/" + str(ip), message)
    
