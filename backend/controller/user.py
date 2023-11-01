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
        """
        User Login
        ---
        tags:
            - User
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token
        responses:
            200:
                description: Login success
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 200
                        token:
                            type: string
                            example: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
                        message:
                            type: string
                            example: login success
                        data:
                            type: object
                            properties:
                                uid:
                                    type: integer
                                    example: 1
                                username:
                                    type: string
                                    example: admin
                                email:
                                    type: string
                                    example: admin@example.com
                                phone:
                                    type: string
                                    example: 12345678901
                                role:
                                    type: integer
                                    example: 0
                                last_login:
                                    type: string
                                    example: 2021-01-01 00:00:00
                                last_ip:
                                    type: string
                                    example: 127.0.0.1
            401:
                description: Unauthorized
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 401
                        message:
                            type: string
                            example: token not found
                        data:
                            type: null
            404:
                description: User not found
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 404
                        message:
                            type: string
                            example: user not found
                        data:
                            type: null
        """
        
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
        """
        User Login
        ---
        tags:
            - User
        parameters:
            - in: body
              name: body
              type: object
              properties:
                username:
                    type: string
                    example: admin
                password:
                    type: string
                    example: admin123
        responses:
            200:
                description: Login success
                schema:
                    type: object
                    properties: 
                        code:
                            type: integer
                            example: 200
                        token:
                            type: string
                            example: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
                        message:
                            type: string
                            example: login success
                        data:
                            type: object
                            properties:
                                uid:
                                    type: integer
                                    example: 1
                                username:
                                    type: string
                                    example: admin
                                email:
                                    type: string
                                    example: admin@example.com
                                phone:
                                    type: string
                                    example: 12345678901
                                role:
                                    type: integer
                                    example: 0
                                last_login:
                                    type: string
                                    example: 2021-01-01 00:00:00
                                last_ip:
                                    type: string
                                    example: 127.0.0.1
            401:
                description: Unauthorized
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 401
                        message:
                            type: string
                            example: token not found
                        data:
                            type: null
            404:
                description: User not found
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 404
                        message:
                            type: string
                            example: user not found
                        data:
                            type: null
                            
        """        
        
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
        """
        User Logout
        ---
        tags:
            - User
        responses:
            200:
                description: Logout success
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 200
                        message:
                            type: string
                            example: logout success
                        data:
                            type: null
        """
        
        return BasicResponse(HTTPStatus.OK, "logout success", None)
    
class UserAdd(Resource):
    @marshal_with(basic_response)
    def post(self):
        """
        User Register
        ---
        tags:
            - User
        parameters:
            - in: body
              name: body
              type: object
              properties:
                username:
                    type: string
                    example: admin
                password:
                    type: string
                    example: admin123
                email:
                    type: string
                    example: admin@example.com
                phone:
                    type: string
                    example: 12345678901
        responses:
            200:
                description: Register success
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 200
                        message:
                            type: string
                            example: register success
                        data:
                            type: object
                            properties:
                                uid:
                                    type: integer
                                    example: 1
                                username:
                                    type: string
                                    example: admin
                                email:
                                    type: string
                                    example: admin@example.com
                                phone:
                                    type: string
                                    example: 12345678901
                                role:
                                    type: integer
                                    example: 0
                                last_login:
                                    type: string
                                    example: 2021-01-01 00:00:00
                                last_ip:
                                    type: string
                                    example: 127.0.0.1
            400:
                description: Data format error
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 400
                        message:
                            type: string
                            example: username length error
                        data:
                            type: null
            409:
                description: User already exist
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 409
                        message:
                            type: string
                            example: user already exist
                        data:
                            type: null
        """
        
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
        """
        Get User Info
        ---
        tags:
            - User
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token
        responses:
            200:
                description: Get user info success
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 200
                        token:
                            type: string
                            example: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
                        message:
                            type: string
                            example: get user info success
                        data:
                            type: object
                            properties:
                                uid:
                                    type: integer
                                    example: 1
                                username:
                                    type: string
                                    example: admin
                                email:
                                    type: string
                                    example: admin@example.com
                                phone:
                                    type: string
                                    example: 12345678901
                                role:
                                    type: integer
                                    example: 0
                                last_login:
                                    type: string
                                    example: 2021-01-01 00:00:00
                                last_ip:
                                    type: string
                                    example: 127.0.0.1
            404:
                description: User not found
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 404
                        message:
                            type: string
                            example: user not found
                        data:
                            type: null
        """
        
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
    def post(self, uid):
        """
        Update User Info
        ---
        tags:
            - User
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token
            - in: path
              name: uid
              type: integer
              required: true
              description: User ID
            - in: body
              name: body
              type: object
              properties:
                password:
                    type: string
                    example: admin123
                email:
                    type: string
                    example: admin@example.com
                phone:
                    type: string
                    example: 12345678901
        responses:
            200:
                description: Update user info success
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 200
                        token:
                            type: string
                            example: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
                        message:
                            type: string
                            example: update user info success
                        data:
                            type: object
                            properties:
                                uid:
                                    type: integer
                                    example: 1
                                username:
                                    type: string
                                    example: admin
                                email:
                                    type: string
                                    example: admin@example.com
                                phone:
                                    type: string
                                    example: 12345678901
                                role:
                                    type: integer
                                    example: 0
                                last_login:
                                    type: string
                                    example: 2021-01-01 00:00:00
                                last_ip:
                                    type: string
                                    example: 127.0.0.1
            400:
                description: Data format error
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 400
                        message:
                            type: string
                            example: password length error
                        data:
                            type: null
            401:
                description: Unauthorized
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 401
                        message:
                            type: string
                            example: user not found
                        data:
                            type: null
            404:
                description: User not found
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 404
                        message:
                            type: string
                            example: user not found
                        data:
                            type: null
            409:
                description: Email already exist
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 409
                        message:
                            type: string
                            example: email already exist
                        data:
                            type: null
        """
        
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str, required=False)
        parser.add_argument('email', type=str, required=False)
        parser.add_argument('phone', type=str, required=False)
        args = parser.parse_args(strict=False)
                
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if user is None or (user.role != 0 and user.uid != uid):
            return BasicResponse(HTTPStatus.UNAUTHORIZED, "user not found", None)
        user = User.query.filter_by(uid=uid).first()
        
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
                user_email = User.query.filter_by(email=args['email']).first()
                if user_email is not None and user_email.uid != uid:
                    return BasicResponse(HTTPStatus.CONFLICT, "email already exist", None)
                user.email = args['email']
            if args['phone'] is not None:
                user.phone = args['phone']
            db.session.commit()
            udata = marshal(user, user_data)
            return BasicResponse(HTTPStatus.OK, "update user info success", udata)
        
class UserDelete(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def post(self, uid):
        """
        Delete User
        ---
        tags:
            - User
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token
            - in: path
              name: uid
              type: integer
              required: true
              description: User ID
        responses:
            200:
                description: Delete user success
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 200
                        token:
                            type: string
                            example: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
                        message:
                            type: string
                            example: delete user success
                        data:
                            type: null
            401:
                description: Unauthorized
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 401
                        message:
                            type: string
                            example: user not found
                        data:
                            type: null
        """
        
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        
        if user is None or (user.role != 0 and user.uid != uid):
            return BasicResponse(HTTPStatus.UNAUTHORIZED, "user not found", None)
        else:
            user = User.query.filter_by(uid=uid).first()
            db.session.delete(user)
            db.session.commit()
            return BasicResponse(HTTPStatus.OK, "delete user success", None)
        
class UserList(Resource):
    @marshal_with(basic_response)
    @jwt_required()
    def get(self):
        """
        Get User List
        ---
        tags:
            - User
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token
        responses:
            200:
                description: Get user list success
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 200
                        token:
                            type: string
                            example: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
                        message:
                            type: string
                            example: get user list success
                        data:
                            type: array
                            items:
                                type: object
                                properties:
                                    uid:
                                        type: integer
                                        example: 1
                                    username:
                                        type: string
                                        example: admin
                                    email:
                                        type: string
                                        example: admin@example.com
                                    phone:
                                        type: string
                                        example: 12345678901
                                    role:
                                        type: integer
                                        example: 0
                                    last_login:
                                        type: string
                                        example: 2021-01-01 00:00:00
                                    last_ip:
                                        type: string
                                        example: 127.0.0.1
            404:
                description: User not found
                schema:
                    type: object
                    properties:
                        code:
                            type: integer
                            example: 404
                        message:
                            type: string
                            example: user not found
                        data:
                            type: null
        """
        
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            return BasicResponse(HTTPStatus.NOT_FOUND, "user not found", None)
        elif user.role != 0:
            udata = marshal(user, user_data)
            return BasicResponse(HTTPStatus.OK, "get user list success", udata)
        else:
            users = User.query.all()
            udata = marshal(users, user_data)
            return BasicResponse(HTTPStatus.OK, "get user list success", udata)