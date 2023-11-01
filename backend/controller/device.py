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

class DeviceList(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def get(self):
        """
        Get device list.
        ---
        tags:
            - device
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: The token value.
        responses:
            200:
                description: Get device list success.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 200
                        token:
                            type: string
                            description: The token value.
                            example: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsInVzZXJuYW1lIjoiYWRtaW4iLCJleHAiOjE2MjE1NjQxNzMsImlhdCI6MTYyMTU2MjU3M30.8J5RmX7Yy2QY0J6Q5WdYbZvX7n1r6qO9kX8cI6Wj0VU
                        message:
                            type: string
                            description: The response message.
                            example: get device list success
                        data:
                            type: array
                            description: The device list.
                            items:
                                type: object
                                properties:
                                    did:
                                        type: integer
                                        description: The device id.
                                        example: 1
                                    uid:
                                        type: integer
                                        description: The user id.
                                        example: 1
                                    name:
                                        type: string
                                        description: The device name.
                                        example: device1
                                    description:
                                        type: string
                                        description: The device description.
                                        example: this is a device
                                    type:
                                        type: integer
                                        description: The device type.
                                        example: 0
                                    status:
                                        type: integer
                                        description: The device status.
                                        example: 0
                                    ip:
                                        type: string
                                        description: The device ip.
                                        example: 127.0.0.1
                                    longitude:
                                        type: float
                                        description: The device longitude.
                                        example: 0
                                    latitude:
                                        type: float
                                        description: The device latitude.
                                        example: 0
            401:
                description: Token not found.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 401
                        message:
                            type: string
                            description: The response message.
                            example: token not found
            404:
                description: User not found.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 404
                        message:
                            type: string
                            description: The response message.
                            example: user not found
        """
        
        token = request.headers.get('Authorization')
        if token is None:
            return BasicResponse(HTTPStatus.UNAUTHORIZED, "token not found", None)
        else:
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()
            if user is None:
                return BasicResponse(HTTPStatus.NOT_FOUND, "user not found", None)
            if user.role == 0:
                devices = Device.query.all()
            else:
                devices = Device.query.filter_by(uid=user.uid).all()
            if devices is None:
                return BasicResponse(HTTPStatus.NOT_FOUND, "device not found", None)
            ddata = marshal(devices, device_data)
            return BasicResponse(HTTPStatus.OK, "get device list success", ddata, token)
        
class DeviceAdd(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def post(self):
        """
        Add device.
        ---
        tags:
            - device
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: The token value.
            - in: body
              name: body
              type: object
              required: true
              description: The device info.
              properties:
                name:
                    type: string
                    description: The device name.
                    example: device1
                description:
                    type: string
                    description: The device description.
                    example: this is a device
                type:
                    type: integer
                    description: The device type.
                    example: 0
                status:
                    type: integer
                    description: The device status.
                    example: 0
                ip:
                    type: string
                    description: The device ip.
                    example: 127.0.0.1
                longitude:
                    type: float
                    description: The device longitude.
                    example: 0
                latitude:
                    type: float
                    description: The device latitude.
                    example: 0
        responses:
            200:
                description: Add device success.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 200
                        token:
                            type: string
                            description: The token value.
                            example: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsInVzZXJuYW1lIjoiYWRtaW4iLCJleHAiOjE2MjE1NjQxNzMsImlhdCI6MTYyMTU2MjU3M30.8J5RmX7Yy2QY0J6Q5WdYbZvX7n1r6qO9kX8cI6Wj0VU
                        message:
                            type: string
                            description: The response message.
                            example: add device success
                        data:
                            type: object
                            description: The device info.
                            properties:
                                did:
                                    type: integer
                                    description: The device id.
                                    example: 1
                                uid:
                                    type: integer
                                    description: The user id.
                                    example: 1
                                name:
                                    type: string
                                    description: The device name.
                                    example: device1
                                description:
                                    type: string
                                    description: The device description.
                                    example: this is a device
                                type:
                                    type: integer
                                    description: The device type.
                                    example: 0
                                status:
                                    type: integer
                                    description: The device status.
                                    example: 0
                                ip:
                                    type: string
                                    description: The device ip.
                                    example: 127.0.0.1
                                longitude:
                                    type: float
                                    description: The device longitude.
                                    example: 0
                                latitude:
                                    type: float
                                    description: The device latitude.
                                    example: 0
            400:
                description: Data format error.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 400
                        message:
                            type: string
                            description: The response message.
                            example: device name too long
            401:
                description: Token not found.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 401
                        message:
                            type: string
                            description: The response message.
                            example: token not found
            404:
                description: User not found.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 404
                        message:
                            type: string
                            description: The response message.
                            example: user not found
        """
        
        token = request.headers.get('Authorization')
        if token is None:
            return BasicResponse(HTTPStatus.UNAUTHORIZED, "token not found", None)
        else:
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()
            if user is None:
                return BasicResponse(HTTPStatus.NOT_FOUND, "user not found", None)
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True)
            parser.add_argument('description', type=str, required=False)
            parser.add_argument('type', type=int, required=True)
            parser.add_argument('status', type=int, required=True)
            parser.add_argument('ip', type=str, required=True)
            parser.add_argument('longitude', type=float, required=False)
            parser.add_argument('latitude', type=float, required=False)
            args = parser.parse_args(strict=False)
            # print(args)
            
            name = args['name']
            description = args['description']
            type = args['type']
            status = args['status']
            ip = args['ip']
            longitude = args['longitude']
            latitude = args['latitude']
            
            if len(name) > 20:
                return BasicResponse(HTTPStatus.BAD_REQUEST, "device name too long", None)
            if description is not None and len(description) > 100:
                return BasicResponse(HTTPStatus.BAD_REQUEST, "device description too long", None)
            if type != 0 and type != 1:
                return BasicResponse(HTTPStatus.BAD_REQUEST, "device type error", None)
            if status != 0 and status != 1:
                return BasicResponse(HTTPStatus.BAD_REQUEST, "device status error", None)
            if not checkIPV4(ip):
                return BasicResponse(HTTPStatus.BAD_REQUEST, "device ip format error", None)
            if longitude is not None and (longitude < -180 or longitude > 180):
                return BasicResponse(HTTPStatus.BAD_REQUEST, "device longitude error", None)
            if latitude is not None and (latitude < -90 or latitude > 90):
                return BasicResponse(HTTPStatus.BAD_REQUEST, "device latitude error", None)
            
            device = Device(
                uid=user.uid,
                name=name,
                description=description,
                type=type,
                status=status,
                ip=ip,
                longitude=longitude,
                latitude=latitude
            )
            db.session.add(device)
            db.session.commit()
            ddata = marshal(device, device_data)
            return BasicResponse(HTTPStatus.OK, "add device success", ddata, token)
        
class DeviceInfo(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def get(self, did):
        """
        Get device info.
        ---
        tags:
            - device
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: The token value.
            - in: path
              name: did
              type: integer
              required: true
              description: The device id.
        responses:
            200:
                description: Get device info success.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 200
                        token:
                            type: string
                            description: The token value.
                            example: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsInVzZXJuYW1lIjoiYWRtaW4iLCJleHAiOjE2MjE1NjQxNzMsImlhdCI6MTYyMTU2MjU3M30.8J5RmX7Yy2QY0J6Q5WdYbZvX7n1r6qO9kX8cI6Wj0VU
                        message:
                            type: string
                            description: The response message.
                            example: get device info success
                        data:
                            type: object
                            description: The device info.
                            properties:
                                did:
                                    type: integer
                                    description: The device id.
                                    example: 1
                                uid:
                                    type: integer
                                    description: The user id.
                                    example: 1
                                name:
                                    type: string
                                    description: The device name.
                                    example: device1
                                description:
                                    type: string
                                    description: The device description.
                                    example: this is a device
                                type:
                                    type: integer
                                    description: The device type.
                                    example: 0
                                status:
                                    type: integer
                                    description: The device status.
                                    example: 0
                                ip:
                                    type: string
                                    description: The device ip.
                                    example: 127.0.0.1
                                longitude:
                                    type: float
                                    description: The device longitude.
                                    example: 0
                                latitude:  
                                    type: float
                                    description: The device latitude.
                                    example: 0
            401:
                description: Token not found.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 401
                        message:
                            type: string
                            description: The response message.
                            example: token not found
            404:
                description: User not found.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 404
                        message:
                            type: string
                            description: The response message.
                            example: user not found
        """
        
        token = request.headers.get('Authorization')
        if token is None:
            return BasicResponse(HTTPStatus.UNAUTHORIZED, "token not found", None)
        else:
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()
            if user is None:
                return BasicResponse(HTTPStatus.NOT_FOUND, "user not found", None)
            if user.role == 0:
                device = Device.query.filter_by(did=did).first()
            else:
                device = Device.query.filter_by(did=did, uid=user.uid).first()
            if device is None:
                return BasicResponse(HTTPStatus.NOT_FOUND, "device not found", None)
            ddata = marshal(device, device_data)
            return BasicResponse(HTTPStatus.OK, "get device info success", ddata, token)
        
class DeviceUpdate(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def post(self, did):
        """
        Update device info.
        ---
        tags:
            - device
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: The token value.
            - in: path
              name: did
              type: integer
              required: true
              description: The device id.
            - in: body
              name: body
              type: object
              required: true
              description: The device info.
              properties:
                name:
                    type: string
                    description: The device name.
                    example: device1
                description:
                    type: string
                    description: The device description.
                    example: this is a device
                type:
                    type: integer
                    description: The device type.
                    example: 0
                status:
                    type: integer
                    description: The device status.
                    example: 0
                ip:
                    type: string
                    description: The device ip.
                    example: 127.0.0.1
                longitude:
                    type: float
                    description: The device longitude.
                    example: 0
                latitude:
                    type: float
                    description: The device latitude.
                    example: 0
        responses:
            200:
                description: Update device info success.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 200
                        token:
                            type: string
                            description: The token value.
                            example: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsInVzZXJuYW1lIjoiYWRtaW4iLCJleHAiOjE2MjE1NjQxNzMsImlhdCI6MTYyMTU2MjU3M30.8J5RmX7Yy2QY0J6Q5WdYbZvX7n1r6qO9kX8cI6Wj0VU
                        message:
                            type: string
                            description: The response message.
                            example: update device success
                        data:
                            type: object
                            description: The device info.
                            properties:
                                did:
                                    type: integer
                                    description: The device id.
                                    example: 1
                                uid:
                                    type: integer
                                    description: The user id.
                                    example: 1
                                name:
                                    type: string
                                    description: The device name.
                                    example: device1
                                description:
                                    type: string
                                    description: The device description.
                                    example: this is a device
                                type:
                                    type: integer
                                    description: The device type.
                                    example: 0
                                status:
                                    type: integer
                                    description: The device status.
                                    example: 0
                                ip:
                                    type: string
                                    description: The device ip.
                                    example: 127.0.0.1
                                longitude:
                                    type: float
                                    description: The device longitude.
                                    example: 0
                                latitude:
                                    type: float
                                    description: The device latitude.
                                    example: 0
            400:
                description: Data format error.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 400
                        message:
                            type: string
                            description: The response message.
                            example: device name too long
            401:
                description: Token not found.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 401
                        message:
                            type: string
                            description: The response message.
                            example: token not found
            404:
                description: User not found.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 404
                        message:
                            type: string
                            description: The response message.
                            example: user not found
        """
        
        token = request.headers.get('Authorization')
        if token is None:
            return BasicResponse(HTTPStatus.UNAUTHORIZED, "token not found", None)
        else:
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()
            if user is None:
                return BasicResponse(HTTPStatus.NOT_FOUND, "user not found", None)
            if user.role == 0:
                device = Device.query.filter_by(did=did).first()
            else:
                device = Device.query.filter_by(did=did, uid=user.uid).first()
            if device is None:
                return BasicResponse(HTTPStatus.NOT_FOUND, "device not found", None)
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=False)
            parser.add_argument('description', type=str, required=False)
            # parser.add_argument('type', type=int, required=False)
            parser.add_argument('status', type=int, required=False)
            parser.add_argument('ip', type=str, required=False)
            parser.add_argument('longitude', type=float, required=False)
            parser.add_argument('latitude', type=float, required=False)
            args = parser.parse_args(strict=False)
            
            if args['name'] is not None: 
                if len(args['name']) > 20:
                    return BasicResponse(HTTPStatus.BAD_REQUEST, "device name too long", None)
                device.name = args['name']
            if args['description'] is not None: 
                if len(args['description']) > 100:
                    return BasicResponse(HTTPStatus.BAD_REQUEST, "device description too long", None)
                device.description = args['description']
            if args['status'] is not None: 
                if args['status'] != 0 and args['status'] != 1:
                    return BasicResponse(HTTPStatus.BAD_REQUEST, "device status error", None)
                device.status = args['status']
            if args['ip'] is not None: 
                if not checkIPV4(args['ip']):
                    return BasicResponse(HTTPStatus.BAD_REQUEST, "device ip format error", None)
                device.ip = args['ip']
            if args['longitude'] is not None:
                if args['longitude'] < -180 or args['longitude'] > 180:
                    return BasicResponse(HTTPStatus.BAD_REQUEST, "device longitude error", None)
                device.longitude = args['longitude']
            if args['latitude'] is not None:
                if args['latitude'] < -90 or args['latitude'] > 90:
                    return BasicResponse(HTTPStatus.BAD_REQUEST, "device latitude error", None)
                device.latitude = args['latitude']
            
            db.session.commit()
            ddata = marshal(device, device_data)
            return BasicResponse(HTTPStatus.OK, "update device success", ddata, token)
        
class DeviceDelete(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def post(self, did):
        """
        Delete device.
        ---
        tags:
            - device
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: The token value.
            - in: path
              name: did
              type: integer
              required: true
              description: The device id.
        responses:
            200:
                description: Delete device success.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 200
                        token:
                            type: string
                            description: The token value.
                            example: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsInVzZXJuYW1lIjoiYWRtaW4iLCJleHAiOjE2MjE1NjQxNzMsImlhdCI6MTYyMTU2MjU3M30.8J5RmX7Yy2QY0J6Q5WdYbZvX7n1r6qO9kX8cI6Wj0VU
                        message:
                            type: string
                            description: The response message.
                            example: delete device success
                        data:
                            type: object
                            description: The device info.
                            properties:
                                did:
                                    type: integer
                                    description: The device id.
                                    example: 1
                                uid:
                                    type: integer
                                    description: The user id.
                                    example: 1
                                name:
                                    type: string
                                    description: The device name.
                                    example: device1
                                description:
                                    type: string
                                    description: The device description.
                                    example: this is a device
                                type:
                                    type: integer
                                    description: The device type.
                                    example: 0
                                status:
                                    type: integer
                                    description: The device status.
                                    example: 0
                                ip:
                                    type: string
                                    description: The device ip.
                                    example: 127.0.0.1
                                longitude: 
                                    type: float
                                    description: The device longitude.
                                    example: 0
                                latitude:
                                    type: float
                                    description: The device latitude.
                                    example: 0
            401:
                description: Token not found.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 401
                        message:
                            type: string
                            description: The response message.
                            example: token not found
            404:
                description: User not found.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 404
                        message:
                            type: string
                            description: The response message.
                            example: user not found
        """
        
        token = request.headers.get('Authorization')
        if token is None:
            return BasicResponse(HTTPStatus.UNAUTHORIZED, "token not found", None)
        else:
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()
            if user is None:
                return BasicResponse(HTTPStatus.NOT_FOUND, "user not found", None)
            if user.role == 0:
                device = Device.query.filter_by(did=did).first()
            else:
                device = Device.query.filter_by(did=did, uid=user.uid).first()
            if device is None:
                return BasicResponse(HTTPStatus.NOT_FOUND, "device not found", None)
            db.session.delete(device)
            db.session.commit()
            ddata = marshal(device, device_data)
            return BasicResponse(HTTPStatus.OK, "delete device success", ddata, token)

class DeviceData(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def get(self, did):
        """ 
        Get device data.
        ---
        tags:
            - device
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: The token value.
            - in: path
              name: did
              type: integer
              required: true
              description: The device id.
        responses:
            200:
                description: Get device data success.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 200
                        token:
                            type: string
                            description: The token value.
                            example: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsInVzZXJuYW1lIjoiYWRtaW4iLCJleHAiOjE2MjE1NjQxNzMsImlhdCI6MTYyMTU2MjU3M30.8J5RmX7Yy2QY0J6Q5WdYbZvX7n1r6qO9kX8cI6Wj0VU
                        message:
                            type: string
                            description: The response message.
                            example: get sensor data success
                        data:
                            type: array
                            description: The sensor data.
                            items:
                                type: object
                                properties:
                                    sdid:
                                        type: integer
                                        description: The sensor data id.
                                        example: 1
                                    did:
                                        type: integer
                                        description: The device id.
                                        example: 1
                                    level:
                                        type: integer
                                        description: The sensor data level.
                                        example: 0
                                    message:
                                        type: string
                                        description: The sensor data message.
                                        example: this is a sensor data
                                    timestamp:
                                        type: integer
                                        description: The sensor data timestamp.
                                        example: 1621567000
                                    data:
                                        type: float
                                        description: The sensor data.
                                        example: 1.0
            400:
                description: Data format error.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 400
                        message:
                            type: string
                            description: The response message.
                            example: device type error
            401:
                description: Token not found.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 401
                        message:
                            type: string
                            description: The response message.
                            example: token not found
            404:
                description: User not found.
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            description: The response code.
                            example: 404
                        message:
                            type: string
                            description: The response message.
                            example: user not found
        """
        
        token = request.headers.get('Authorization')
        if token is None:
            return BasicResponse(HTTPStatus.UNAUTHORIZED, "token not found", None)
        else:
            username = get_jwt_identity()
            user = User.query.filter_by(username=username).first()
            if user is None:
                return BasicResponse(HTTPStatus.NOT_FOUND, "user not found", None)
            if user.role == 0:
                device = Device.query.filter_by(did=did).first()
            else:
                device = Device.query.filter_by(did=did, uid=user.uid).first()
            if device is None:
                return BasicResponse(HTTPStatus.NOT_FOUND, "device not found", None)
            if device.type == 0:
                sensors = SensorData.query.filter_by(did=did).all()
                sdata = marshal(sensors, sensor_data)
                return BasicResponse(HTTPStatus.OK, "get sensor data success", sdata, token)
            elif device.type == 1:
                actuators = ActuatorData.query.filter_by(did=did).all()
                adata = marshal(actuators, actuator_data)
                return BasicResponse(HTTPStatus.OK, "get actuator data success", adata, token)
            return BasicResponse(HTTPStatus.BAD_REQUEST, "device type error", None)