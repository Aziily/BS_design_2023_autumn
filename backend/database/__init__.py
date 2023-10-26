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
    db.session.add(User("admin", "admin", "", "", 0))
    db.session.add(User("user", "user", "", "", 1))
    db.session.commit()