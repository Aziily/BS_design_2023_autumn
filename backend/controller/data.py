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
        parser.add_argument('level', type=int, required=True)
        parser.add_argument('message', type=str, required=True)
        parser.add_argument('timestamp', type=int, required=True)
        parser.add_argument('data', type=float, required=True)
        args = parser.parse_args(strict=False)
        
        ip = request.remote_addr
        if not checkIPV4(ip):
            return BasicResponse(HTTPStatus.BAD_REQUEST, "invalid ip address", None)
        device = Device.query.filter_by(ip=ip, type=0).first()
        if device is None:
            return BasicResponse(HTTPStatus.NOT_FOUND, "device not found", None)
        timestamp = args['timestamp']
        data = args['data']
        if args['level'] not in [0, 1, 2]:
            return BasicResponse(HTTPStatus.BAD_REQUEST, "invalid level", None)
        level = args['level']
        if args['message'] is None or len(args['message']) > 100:
            return BasicResponse(HTTPStatus.BAD_REQUEST, "invalid message", None)
        message = args['message']
        sensor_data = SensorData(device.did, level, message, timestamp, data)
        db.session.add(sensor_data)
        db.session.commit()
        return BasicResponse(HTTPStatus.OK, "add sensor data success", None)
    
class ActuatorDataAdd(Resource):
    @marshal_with(basic_response)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('level', type=int, required=True)
        parser.add_argument('message', type=str, required=True)
        parser.add_argument('timestamp', type=int, required=True)
        parser.add_argument('data', type=bool, required=True)
        args = parser.parse_args(strict=False)
        
        ip = request.remote_addr
        if not checkIPV4(ip):
            return BasicResponse(HTTPStatus.BAD_REQUEST, "invalid ip address", None)
        device = Device.query.filter_by(ip=ip, type=1).first()
        if device is None:
            return BasicResponse(HTTPStatus.NOT_FOUND, "device not found", None)
        timestamp = args['timestamp']
        data = args['data']
        if args['level'] not in [0, 1, 2]:
            return BasicResponse(HTTPStatus.BAD_REQUEST, "invalid level", None)
        level = args['level']
        if args['message'] is None or len(args['message']) > 100:
            return BasicResponse(HTTPStatus.BAD_REQUEST, "invalid message", None)
        message = args['message']
        actuator_data = ActuatorData(device.did, level, message, timestamp, data)
        db.session.add(actuator_data)
        db.session.commit()
        return BasicResponse(HTTPStatus.OK, "add actuator data success", None)
    
class DataList(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=int, required=False)
        parser.add_argument('level', type=int, required=False)
        parser.add_argument('year', type=int, required=False)
        parser.add_argument('month', type=int, required=False)
        parser.add_argument('day', type=int, required=False)
        args = parser.parse_args(strict=False)
        
        type = args['type']
        level = args['level']
        year = args['year']
        month = args['month']
        day = args['day']
        
        sensor_datas = None
        actuator_datas = None
        
        timestamp_from = time.mktime((
            year if year is not None else 1970,
            month if month is not None else 1,
            day if day is not None else 1,
            0, 0, 0, 0, 0, 0
        ))
        timestamp_to = time.mktime((
            year + 1 if year is not None else time.localtime().tm_year + 1,
            month + 1 if month is not None else 1,
            day + 1 if day is not None else 1,
            0, 0, 0, 0, 0, 0
        ))
        
        if type is None:
            if level is None:
                sensor_datas = SensorData.query.filter(
                    SensorData.timestamp >= timestamp_from,
                    SensorData.timestamp < timestamp_to
                ).all()
                actuator_datas = ActuatorData.query.filter(
                    ActuatorData.timestamp >= timestamp_from,
                    ActuatorData.timestamp < timestamp_to
                ).all()
                sdata = marshal(sensor_datas, sensor_data)
                adata = marshal(actuator_datas, actuator_data)
                return BasicResponse(HTTPStatus.OK, "get data success", {
                    'sensor': sdata,
                    'actuator': adata
                })
            else:
                sensor_datas = SensorData.query.filter(
                    SensorData.level == level,
                    SensorData.timestamp >= timestamp_from,
                    SensorData.timestamp < timestamp_to
                ).all()
                actuator_datas = ActuatorData.query.filter(
                    ActuatorData.level == level,
                    ActuatorData.timestamp >= timestamp_from,
                    ActuatorData.timestamp < timestamp_to
                ).all()
                sdata = marshal(sensor_datas, sensor_data)
                adata = marshal(actuator_datas, actuator_data)
                return BasicResponse(HTTPStatus.OK, "get data success", {
                    'sensor': sdata,
                    'actuator': adata
                })
        else:
            if type == 0:
                if level is None:
                    sensor_datas = SensorData.query.filter(
                        SensorData.timestamp >= timestamp_from,
                        SensorData.timestamp < timestamp_to
                    ).all()
                    sdata = marshal(sensor_datas, sensor_data)
                    return BasicResponse(HTTPStatus.OK, "get data success", {
                        'sensor': sdata
                    })
                else:
                    sensor_datas = SensorData.query.filter(
                        SensorData.level == level,
                        SensorData.timestamp >= timestamp_from,
                        SensorData.timestamp < timestamp_to
                    ).all()
                    sdata = marshal(sensor_datas, sensor_data)
                    return BasicResponse(HTTPStatus.OK, "get data success", {
                        'sensor': sdata
                    })
            elif type == 1:
                if level is None:
                    actuator_datas = ActuatorData.query.filter(
                        ActuatorData.timestamp >= timestamp_from,
                        ActuatorData.timestamp < timestamp_to
                    ).all()
                    adata = marshal(actuator_datas, actuator_data)
                    return BasicResponse(HTTPStatus.OK, "get data success", {
                        'actuator': adata
                    })
                else:
                    actuator_datas = ActuatorData.query.filter(
                        ActuatorData.level == level,
                        ActuatorData.timestamp >= timestamp_from,
                        ActuatorData.timestamp < timestamp_to
                    ).all()
                    adata = marshal(actuator_datas, actuator_data)
                    return BasicResponse(HTTPStatus.OK, "get data success", {
                        'actuator': adata
                    })
            else:
                return BasicResponse(HTTPStatus.BAD_REQUEST, "invalid type", None)