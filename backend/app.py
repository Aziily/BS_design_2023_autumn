import datetime
import flask
from flask import Flask
from flask_restful import Api
from exts import db, api, jwt, swagger
from omegaconf import OmegaConf
import os
import sys

conf = OmegaConf.load("config.yaml")
global app
app = Flask(__name__)

class Config(object):
    # database
    user = conf.database.user
    password = conf.database.password
    database = conf.database.database
    ip = conf.database.ip
    port = conf.database.port
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (user, password, ip, port, database)

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = conf.database.SQLALCHEMY_TRACK_MODIFICATIONS
    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = conf.database.SQLALCHEMY_ECHO
    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = conf.database.SQLALCHEMY_COMMIT_ON_TEARDOWN
    
    # jwt
    app.config["JWT_SECRET_KEY"] = conf.jwt.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=conf.jwt.JWT_ACCESS_TOKEN_EXPIRES)
    
app.config.from_object(Config)

db.init_app(app)
api.app = app
api.init_app(app)
jwt.init_app(app)
swagger.init_app(app)
 
if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    args = sys.argv
    
    # has argument and argument is "init"
    if len(args) > 1 and args[1] == "init":
        import database
        with app.app_context():
            database.Initialize()
        exit(0)

    import router    
    router.Initialize()
    
    from gevent.pywsgi import WSGIServer
    # app.run(host=conf.service.host, port=conf.service.port, debug=conf.service.debug)
    web_server = WSGIServer((conf.service.host, int(conf.service.port)), app)
    web_server.serve_forever()
