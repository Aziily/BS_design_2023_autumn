import flask

global db, api, jwt

# database
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
db = SQLAlchemy()

# router
from flask_restful import Api
api = Api()

# jwt
from flask_jwt_extended import JWTManager
jwt = JWTManager()

from flasgger import Swagger
swagger = Swagger()
 