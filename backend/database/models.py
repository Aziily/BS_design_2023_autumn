from sqlalchemy.orm import Mapped, mapped_column

from exts import db

class User(db.Model):
    uid: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(db.String(20), nullable=False)
    password: Mapped[str] = mapped_column(db.String(20), nullable=False)
    email: Mapped[str] = mapped_column(db.String(20), nullable=True)
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
    type: Mapped[int] = mapped_column(db.Integer, nullable=False)
    status: Mapped[int] = mapped_column(db.Integer, nullable=False)
    ip: Mapped[str] = mapped_column(db.String(20), nullable=True)
    
    def __init__(self, uid, name, description, type, status, ip):
        self.uid = uid
        self.name = name
        self.description = description
        self.type = type
        self.status = status
        self.ip = ip
    
    def __repr__(self):
        return '<Device %r>' % self.name
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        return self.did == other.did
    
    def __hash__(self):
        return hash(self.did)