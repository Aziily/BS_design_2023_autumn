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
    db.session.add(Device(1, "device1", "hello", 0, 0, ""))
    db.session.add(Device(1, "device2", "test", 0, 0, ""))
    db.session.add(Device(1, "device3", "asdiuhasdiuhaisdhaioshdoasfcbuiasdgopiasgdiuassbsbgduias", 0, 1, ""))
    db.session.add(Device(1, "device4", "", 1, 1, ""))
    db.session.add(Device(1, "device5", "", 1, 0, ""))
    
    db.session.commit()