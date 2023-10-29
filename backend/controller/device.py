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
            args = parser.parse_args(strict=True)
            
            name = args['name']
            description = args['description']
            type = args['type']
            status = args['status']
            ip = args['ip']
            
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
            
            device = Device(
                uid=user.uid,
                name=name,
                description=description,
                type=type,
                status=status,
                ip=ip
            )
            db.session.add(device)
            db.session.commit()
            ddata = marshal(device, device_data)
            return BasicResponse(HTTPStatus.OK, "add device success", ddata, token)
        
class DeviceInfo(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def get(self, did):
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
            parser.add_argument('type', type=int, required=False)
            parser.add_argument('status', type=int, required=False)
            parser.add_argument('ip', type=str, required=False)
            args = parser.parse_args(strict=True)
            
            if args['name'] is not None: 
                if len(args['name']) > 20:
                    return BasicResponse(HTTPStatus.BAD_REQUEST, "device name too long", None)
                device.name = args['name']
            if args['description'] is not None: 
                if len(args['description']) > 100:
                    return BasicResponse(HTTPStatus.BAD_REQUEST, "device description too long", None)
                device.description = args['description']
            if args['type'] is not None: 
                if args['type'] != 0 and args['type'] != 1:
                    return BasicResponse(HTTPStatus.BAD_REQUEST, "device type error", None)
                device.type = args['type']
            if args['status'] is not None: 
                if args['status'] != 0 and args['status'] != 1:
                    return BasicResponse(HTTPStatus.BAD_REQUEST, "device status error", None)
                device.status = args['status']
            if args['ip'] is not None: 
                if not checkIPV4(args['ip']):
                    return BasicResponse(HTTPStatus.BAD_REQUEST, "device ip format error", None)
                device.ip = args['ip']
            db.session.commit()
            ddata = marshal(device, device_data)
            return BasicResponse(HTTPStatus.OK, "update device success", ddata, token)
        
class DeviceDelete(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def post(self, did):
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
