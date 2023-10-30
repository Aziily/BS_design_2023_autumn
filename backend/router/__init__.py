from exts import api

from controller.user import *
from controller.device import *
from controller.data import *

def Initialize():
    # use '/api' as prefix
    api.prefix = '/api'
    
    # /user
    api.add_resource(UserRegister, '/user/register')
    api.add_resource(UserLogin, '/user/login')
    api.add_resource(UserLogout, '/user/logout')
    api.add_resource(UserInfo, '/user/info')
    api.add_resource(UserUpdate, '/user/update')
    api.add_resource(UserDelete, '/user/delete')
    
    # /device
    api.add_resource(DeviceList, '/device/list')
    api.add_resource(DeviceAdd, '/device/add')
    api.add_resource(DeviceDelete, '/device/delete/<int:did>')
    api.add_resource(DeviceUpdate, '/device/update/<int:did>')
    api.add_resource(DeviceInfo, '/device/info/<int:did>')
    api.add_resource(DeviceData, '/device/data/<int:did>')
    
    # /data
    api.add_resource(DataList, '/data/list')
    api.add_resource(SensorDataAdd, '/data/sensor/add')
    api.add_resource(ActuatorDataAdd, '/data/actuator/add')