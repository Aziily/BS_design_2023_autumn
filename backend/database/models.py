from sqlalchemy.orm import Mapped, mapped_column

from exts import db

class User(db.Model):
    uid: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(db.String(20), nullable=False)
    password: Mapped[str] = mapped_column(db.String(20), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=True)
    role: Mapped[int] = mapped_column(db.Integer, nullable=False)
    
    last_login: Mapped[str] = mapped_column(db.String(20), nullable=True)
    last_ip: Mapped[str] = mapped_column(db.String(20), nullable=True)
    
    def __init__(self, username, password, email, phone, role):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.role = role
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    def __str__(self):
        return self.username
    
    def __eq__(self, other):
        return self.uid == other.uid
    
    def __hash__(self):
        return hash(self.uid)

class Device(db.Model):
    did: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    uid: Mapped[int] = mapped_column(db.Integer, nullable=False)
    name: Mapped[str] = mapped_column(db.String(20), nullable=False)
    description: Mapped[str] = mapped_column(db.String(100), nullable=True)
    # 0: sensor, 1: actuator
    type: Mapped[int] = mapped_column(db.Integer, nullable=False)
    # 0: offline, 1: online
    status: Mapped[int] = mapped_column(db.Integer, nullable=False)
    ip: Mapped[str] = mapped_column(db.String(20), nullable=False)
    
    longitude: Mapped[float] = mapped_column(db.Float, nullable=True)
    latitude: Mapped[float] = mapped_column(db.Float, nullable=True)
    
    def __init__(self, uid, name, description, type, status, ip, longitude, latitude):
        self.uid = uid
        self.name = name
        self.description = description
        self.type = type
        self.status = status
        self.ip = ip
        self.longitude = longitude
        self.latitude = latitude
    
    def __repr__(self):
        return '<Device %r>' % self.name
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return self.did == other.did
    
    def __hash__(self):
        return hash(self.did)
    
class SensorData(db.Model):
    sdid: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    did: Mapped[int] = mapped_column(db.Integer, nullable=False)
    # 0: INFO, 1: WARNING, 2: ERROR
    level: Mapped[int] = mapped_column(db.Integer, nullable=False)
    message: Mapped[str] = mapped_column(db.String(100), nullable=False)
    # a unix timestamp with unsigned int
    timestamp: Mapped[int] = mapped_column(db.Integer, nullable=False)
    # a float number data
    data: Mapped[float] = mapped_column(db.Float, nullable=False)
    
    def __init__(self, did, level, message, timestamp, data):
        self.did = did
        self.level = level
        self.message = message
        self.timestamp = timestamp
        self.data = data
    
    def __repr__(self):
        return '<SensorData %r>' % self.sdid
    
    def __str__(self):
        return self.sdid
    
    def __eq__(self, other):
        return self.sdid == other.sdid
    
    def __hash__(self):
        return hash(self.sdid)
    
class ActuatorData(db.Model):
    adid: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    did: Mapped[int] = mapped_column(db.Integer, nullable=False)
    # 0: INFO, 1: WARNING, 2: ERROR
    level: Mapped[int] = mapped_column(db.Integer, nullable=False)
    message: Mapped[str] = mapped_column(db.String(100), nullable=False)
    # a unix timestamp with unsigned int
    timestamp: Mapped[int] = mapped_column(db.Integer, nullable=False)
    # a boolean data showing whether the actuator is on or off
    data: Mapped[bool] = mapped_column(db.Boolean, nullable=False)
    
    def __init__(self, did, level, message, timestamp, data):
        self.did = did
        self.level = level
        self.message = message
        self.timestamp = timestamp
        self.data = data
    
    def __repr__(self):
        return '<ActuatorData %r>' % self.adid
    
    def __str__(self):
        return self.adid
    
    def __eq__(self, other):
        return self.adid == other.adid
    
    def __hash__(self):
        return hash(self.adid)