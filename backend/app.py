import flask
from flask import Flask
from flask_restful import Api
from exts import db, api, jwt

global app
app = Flask(__name__)

class Config(object):
    # database
    user = 'root'
    password = ''
    database = 'bs'
    ip = "127.0.0.1"
    port = "3306"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (user, password, ip, port, database)

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True
    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
    
    # jwt
    app.config["JWT_SECRET_KEY"] = "super-secret"

app.config.from_object(Config)

db.init_app(app)
api.app = app
api.init_app(app)
jwt.init_app(app)

from flask_restful import Resource
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
 
if __name__ == '__main__':
    import database
    with app.app_context():
        database.Initialize()
    import router
    router.Initialize()
    app.run()
