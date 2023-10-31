import time
import flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import pymysql
pymysql.install_as_MySQLdb()

from exts import db

from .models import *

def Initialize():
    db.drop_all()
    db.create_all()
    # user
    db.session.add(User("admin", "admin123", "admin@example.com", "", 0))
    db.session.add(User("user", "user123", "user@example.com", "", 1))
    
    # device
    db.session.add(Device(1, "device1", "hello", 0, 0, "10.0.0.1"))
    db.session.add(Device(1, "device2", "test", 0, 0, "10.0.0.2"))
    db.session.add(Device(1, "device3", "asdiuhasdiuhaisdhaioshdoasfcbuiasdgopiasgdiuassbsbgduias", 0, 1, "10.0.0.3"))
    db.session.add(Device(1, "device4", "", 1, 1, "192.168.255.255"))
    db.session.add(Device(1, "device5", "", 1, 0, "192.168.255.254"))
    
    # sensor data
    db.session.add(SensorData(1, 0, "testinfo", time.time(), 20.01))
    db.session.add(SensorData(1, 1, "testwarning", time.time() + 1*60*60, 30.45))
    db.session.add(SensorData(1, 2, "testerror", time.time() + 2*60*60, 40.12))
    db.session.add(SensorData(2, 0, "testinfo", time.mktime(time.strptime("2020-12-31 23:59:59", "%Y-%m-%d %H:%M:%S")), 20.01))
    db.session.add(SensorData(2, 1, "testwarning", time.mktime(time.strptime("2020-6-28 23:59:59", "%Y-%m-%d %H:%M:%S")), 30.45))
    db.session.add(SensorData(2, 2, "testerror", time.mktime(time.strptime("2020-1-7 23:59:59", "%Y-%m-%d %H:%M:%S")), 40.12))
    db.session.add(SensorData(3, 0, "testinfo", time.mktime(time.strptime("2002-12-8 23:59:59", "%Y-%m-%d %H:%M:%S")), 20.01))
    
    # actuator data
    db.session.add(ActuatorData(5, 0, "testinfo", time.time(), True))
    db.session.add(ActuatorData(5, 0, "testinfo", time.time() + 1*60*60, False))
    for i in range(100):
        db.session.add(ActuatorData(5, 0, "testinfo", time.time() + i*60*60, bool(i%2)))
    
    db.session.commit()