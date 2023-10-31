from flask_restful import fields, marshal_with

basic_response = {
    'code': fields.Integer,
    'token': fields.String,
    'message': fields.String,
    'data': fields.Raw
}

user_data = {
    'uid': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'role': fields.Integer,
    'last_login': fields.String,
    'last_ip': fields.String
}

device_data = {
    'did': fields.Integer,
    'uid': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'type': fields.Integer,
    'status': fields.Integer,
    'ip': fields.String,
    'longitude': fields.Float,
    'latitude': fields.Float
}

sensor_data = {
    'sdid': fields.Integer,
    'did': fields.Integer,
    'level': fields.Integer,
    'message': fields.String,
    'timestamp': fields.Integer,
    'data': fields.Float
}

actuator_data = {
    'adid': fields.Integer,
    'did': fields.Integer,
    'level': fields.Integer,
    'message': fields.String,
    'timestamp': fields.Integer,
    'data': fields.Boolean
}

class BasicResponse:
    def __init__(self, code, message, data, token=None):
        self.code = code
        self.message = message
        self.data = data
        self.token = token
        
class Userdata:
    def __init__(self, uid, username, email, phone, role, last_login, last_ip):
        self.uid = uid
        self.username = username
        self.email = email
        self.phone = phone
        self.role = role
        self.last_login = last_login
        self.last_ip = last_ip
    
class Devicedata:
    def __init__(self, did, uid, name, description, type, status, ip, longitude, latitude):
        self.did = did
        self.uid = uid
        self.name = name
        self.description = description
        self.type = type
        self.status = status
        self.ip = ip
        self.longitude = longitude
        self.latitude = latitude
        
class Sensordata:
    def __init__(self, sid, did, timestamp, data):
        self.sid = sid
        self.did = did
        self.timestamp = timestamp
        self.data = data
        
class Actuatordata:
    def __init__(self, aid, did, timestamp, data):
        self.aid = aid
        self.did = did
        self.timestamp = timestamp
        self.data = data