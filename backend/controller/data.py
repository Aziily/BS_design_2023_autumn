from os import access
import time
from exts import db, api, jwt

from flask_restful import Resource, reqparse, fields, marshal_with, marshal
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from http import HTTPStatus

from controller.response import *
from database.models import *
from utils import checkIPV4

class SensorDataAdd(Resource):
    @marshal_with(basic_response)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('timestamp', type=int, required=True)
        parser.add_argument('data', type=float, required=True)
        args = parser.parse_args(strict=True)
        
        ip = request.remote_addr
        if not checkIPV4(ip):
            return BasicResponse(HTTPStatus.BAD_REQUEST, "invalid ip address", None)
        device = Device.query.filter_by(ip=ip).first()
        if device is None:
            return BasicResponse(HTTPStatus.NOT_FOUND, "device not found", None)
        timestamp = args['timestamp']
        data = args['data']
        sensor_data = SensorData(device.did, timestamp, data)
        db.session.add(sensor_data)
        db.session.commit()
        return BasicResponse(HTTPStatus.OK, "add sensor data success", None)
    
class ActuatorDataAdd(Resource):
    @marshal_with(basic_response)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('timestamp', type=int, required=True)
        parser.add_argument('data', type=bool, required=True)
        args = parser.parse_args(strict=True)
        
        ip = request.remote_addr
        if not checkIPV4(ip):
            return BasicResponse(HTTPStatus.BAD_REQUEST, "invalid ip address", None)
        device = Device.query.filter_by(ip=ip).first()
        if device is None:
            return BasicResponse(HTTPStatus.NOT_FOUND, "device not found", None)
        timestamp = args['timestamp']
        data = args['data']
        actuator_data = ActuatorData(device.did, timestamp, data)
        db.session.add(actuator_data)
        db.session.commit()
        return BasicResponse(HTTPStatus.OK, "add actuator data success", None)