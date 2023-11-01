from math import e
from os import access
import time
from tracemalloc import start
from exts import db, api, jwt

from flask_restful import Resource, reqparse, fields, marshal_with, marshal
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from http import HTTPStatus

from controller.response import *
from database.models import *
from utils import checkIPV4

class DataYearList(Resource):
    @marshal_with(basic_response)
    def get(self):
        """
        Get year list of data
        ---
        tags:
            - data
        responses:
            200:
                description: get year list success
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: response code
                            example: 200
                        message:
                            type: string
                            description: response message
                            example: get year list success
                        data:
                            type: array
                            items:
                                type: integer
                                description: year
                                example: 2021
        """
        
        sensor_datas = SensorData.query.all()
        actuator_datas = ActuatorData.query.all()
        # get year list from timestamp
        year_list = []
        for sensor_data in sensor_datas:
            year = time.localtime(sensor_data.timestamp).tm_year
            if year not in year_list:
                year_list.append(year)
        for actuator_data in actuator_datas:
            year = time.localtime(actuator_data.timestamp).tm_year
            if year not in year_list:
                year_list.append(year)
        year_list.sort()
        return BasicResponse(HTTPStatus.OK, "get year list success", year_list)

class DataList(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def post(self):
        """
        Get data list
        ---
        tags:
            - data
        parameters:
            - in: body
              name: body
              required: true
              schema:
                type: object
                properties:
                    type:
                        type: integer
                        description: data type
                        example: 0
                    level:
                        type: integer
                        description: data level
                        example: 0
                    year:
                        type: integer
                        description: year
                        example: 2021
                    month:
                        type: integer
                        description: month
                        example: 1
                    day:
                        type: integer
                        description: day
                        example: 1
        responses:
            200:
                description: get data success
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: response code
                            example: 200
                        message:
                            type: string
                            description: response message
                            example: get data success
                        data:
                            type: object
                            properties:
                                sensor:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            sdid:
                                                type: integer
                                                description: sensor data id
                                                example: 1
                                            did:
                                                type: integer
                                                description: device id
                                                example: 1
                                            level:
                                                type: integer
                                                description: data level
                                                example: 0
                                            message:
                                                type: string
                                                description: message
                                                example: test
                                            timestamp:
                                                type: integer
                                                description: timestamp
                                                example: 1620000000
                                            data:
                                                type: float
                                                description: data
                                                example: 1.0
                                actuator:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            adid:
                                                type: integer
                                                description: actuator data id
                                                example: 1
                                            did:
                                                type: integer
                                                description: device id
                                                example: 1
                                            level:
                                                type: integer
                                                description: data level
                                                example: 0
                                            message:
                                                type: string
                                                description: message
                                                example: test
                                            timestamp:
                                                type: integer
                                                description: timestamp
                                                example: 1620000000
                                            data:
                                                type: boolean
                                                description: data
                                                example: true
            400:
                description: invalid type
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: response code
                            example: 400
                        message:
                            type: string
                            description: response message
                            example: invalid type
                        data:
                            type: null
                            description: null
                            example: null
            401:
                description: user not found
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: response code
                            example: 401
                        message:
                            type: string
                            description: response message
                            example: user not found
                        data:
                            type: null
                            description: null
                            example: null
        """
        
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if user is None:
            return BasicResponse(HTTPStatus.UNAUTHORIZED, "user not found", None)
        devices = Device.query.filter_by(uid=user.uid).all()
        device_list = []
        for device in devices:
            device_list.append(device.did)
        
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
        
        start_year, start_month, start_day = 1971, 1, 1
        end_year, end_month, end_day = time.localtime().tm_year + 1, 1, 1
        if year is not None:
            start_year = year
            if month is not None:
                start_month = month
                if day is not None:
                    start_day = day
                    end_day = day + 1
                    end_month = month
                    end_year = year
                else:
                    start_day = 1
                    end_day = 1
                    end_month = month + 1
                    end_year = year
            else:
                start_day = 1
                start_month = 1
                end_day = 1
                end_month = 1
                end_year = year + 1
        else:
            start_day = 1
            start_month = 1
            start_year = 1971
            end_day = 1
            end_month = 1
            end_year = time.localtime().tm_year + 1
        
        timestamp_from = time.mktime((start_year, start_month, start_day, 0, 0, 0, 0, 0, 0))
        timestamp_to = time.mktime((end_year, end_month, end_day, 0, 0, 0, 0, 0, 0))
        
        if type is None:
            if level is None:
                sensor_datas = SensorData.query.filter(
                    SensorData.timestamp >= timestamp_from,
                    SensorData.timestamp < timestamp_to,
                    SensorData.did.in_(device_list)
                ).all()
                actuator_datas = ActuatorData.query.filter(
                    ActuatorData.timestamp >= timestamp_from,
                    ActuatorData.timestamp < timestamp_to,
                    ActuatorData.did.in_(device_list)
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
                    SensorData.timestamp < timestamp_to,
                    SensorData.did.in_(device_list)
                ).all()
                actuator_datas = ActuatorData.query.filter(
                    ActuatorData.level == level,
                    ActuatorData.timestamp >= timestamp_from,
                    ActuatorData.timestamp < timestamp_to,
                    ActuatorData.did.in_(device_list)
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
                        SensorData.timestamp < timestamp_to,
                        SensorData.did.in_(device_list)
                    ).all()
                    sdata = marshal(sensor_datas, sensor_data)
                    return BasicResponse(HTTPStatus.OK, "get data success", {
                        'sensor': sdata
                    })
                else:
                    sensor_datas = SensorData.query.filter(
                        SensorData.level == level,
                        SensorData.timestamp >= timestamp_from,
                        SensorData.timestamp < timestamp_to,
                        SensorData.did.in_(device_list)
                    ).all()
                    sdata = marshal(sensor_datas, sensor_data)
                    return BasicResponse(HTTPStatus.OK, "get data success", {
                        'sensor': sdata
                    })
            elif type == 1:
                if level is None:
                    actuator_datas = ActuatorData.query.filter(
                        ActuatorData.timestamp >= timestamp_from,
                        ActuatorData.timestamp < timestamp_to,
                        ActuatorData.did.in_(device_list)
                    ).all()
                    adata = marshal(actuator_datas, actuator_data)
                    return BasicResponse(HTTPStatus.OK, "get data success", {
                        'actuator': adata
                    })
                else:
                    actuator_datas = ActuatorData.query.filter(
                        ActuatorData.level == level,
                        ActuatorData.timestamp >= timestamp_from,
                        ActuatorData.timestamp < timestamp_to,
                        ActuatorData.did.in_(device_list)
                    ).all()
                    adata = marshal(actuator_datas, actuator_data)
                    return BasicResponse(HTTPStatus.OK, "get data success", {
                        'actuator': adata
                    })
            else:
                return BasicResponse(HTTPStatus.BAD_REQUEST, "invalid type", None)