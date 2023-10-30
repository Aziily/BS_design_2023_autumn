from os import access
import time
from exts import db, api, jwt

from flask_restful import Resource, reqparse, fields, marshal_with, marshal
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from http import HTTPStatus

from controller.response import *
from database.models import *
from utils.valid import checkEmail

class UserLogin(Resource):
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
            else:
                udata = marshal(user, user_data)
                return BasicResponse(HTTPStatus.OK, "login success", udata, token)
    
    @marshal_with(basic_response)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args(strict=False)
        print(args)
        
        username = args['username']
        password = args['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            return BasicResponse(HTTPStatus.NOT_FOUND, "user not found", None)
        elif user.password != password:
            return BasicResponse(HTTPStatus.UNAUTHORIZED, "password error", None)
        else:
            # copy data
            udata = marshal(user, user_data)
            # update
            user.last_login = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            user.last_ip = request.remote_addr if request.remote_addr is not None else user.last_ip
            db.session.commit()
            access_token = create_access_token(identity=user.username)
            return BasicResponse(HTTPStatus.OK, "login success", udata, "Bearer " + access_token)
        
class UserLogout(Resource):
    @marshal_with(basic_response)
    def get(self):
        return BasicResponse(HTTPStatus.OK, "logout success", None)
    
class UserRegister(Resource):
    @marshal_with(basic_response)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('phone', type=str, required=False)
        args = parser.parse_args(strict=False)
        
        username = args['username']
        password = args['password']
        email = args['email']
        phone = args['phone']
        
        if len(username) < 6 or len(username) > 20:
            return BasicResponse(HTTPStatus.BAD_REQUEST, "username length error", None)
        if len(password) < 6 or len(password) > 20:
            return BasicResponse(HTTPStatus.BAD_REQUEST, "password length error", None)
        if not checkEmail(email):
            return BasicResponse(HTTPStatus.BAD_REQUEST, "email format error", None)
        user = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()
        
        if user is None and user_email is None:
            user = User(username, password, email, phone, 1)
            udata = marshal(user, user_data)
            db.session.add(user)
            db.session.commit()
            return BasicResponse(HTTPStatus.OK, "register success", udata)
        else:
            return BasicResponse(HTTPStatus.CONFLICT, "user already exist", None)
        
class UserInfo(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if user is None:
            return BasicResponse(HTTPStatus.NOT_FOUND, "user not found", None)
        else:
            udata = marshal(user, user_data)
            return BasicResponse(HTTPStatus.OK, "get user info success", udata)
        
class UserUpdate(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str, required=False)
        parser.add_argument('email', type=str, required=False)
        parser.add_argument('phone', type=str, required=False)
        args = parser.parse_args(strict=False)
                
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            return BasicResponse(HTTPStatus.NOT_FOUND, "user not found", None)
        else:
            if args['password'] is not None:
                if len(args['password']) < 6 or len(args['password']) > 20:
                    return BasicResponse(HTTPStatus.BAD_REQUEST, "password length error", None)
                user.password = args['password']
            if args['email'] is not None:
                if not checkEmail(args['email']):
                    return BasicResponse(HTTPStatus.BAD_REQUEST, "email format error", None)
                user.email = args['email']
            if args['phone'] is not None:
                user.phone = args['phone']
            db.session.commit()
            udata = marshal(user, user_data)
            return BasicResponse(HTTPStatus.OK, "update user info success", udata)
        
class UserDelete(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            return BasicResponse(HTTPStatus.NOT_FOUND, "user not found", None)
        else:
            db.session.delete(user)
            db.session.commit()
            return BasicResponse(HTTPStatus.OK, "delete user success", None)