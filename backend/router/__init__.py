from exts import api

from controller.user import *
from controller.device import *

def Initialize():
    api.add_resource(UserRegister, '/user/register')
    api.add_resource(UserLogin, '/user/login')
    api.add_resource(UserLogout, '/user/logout')
    api.add_resource(UserInfo, '/user/info')
    api.add_resource(UserUpdate, '/user/update')