from exts import api

from controller.user import *
from controller.device import *
from controller.data import *

def Initialize():
    # use '/api' as prefix
    api.prefix = '/api'
    
    # /user
    api.add_resource(UserList, '/user/list')
    api.add_resource(UserAdd, '/user/add')
    api.add_resource(UserLogin, '/user/login')
    api.add_resource(UserLogout, '/user/logout')
    api.add_resource(UserInfo, '/user/info')
    api.add_resource(UserUpdate, '/user/update/<int:uid>')
    api.add_resource(UserDelete, '/user/delete/<int:uid>')
    
    # /device
    api.add_resource(DeviceList, '/device/list')
    api.add_resource(DeviceAdd, '/device/add')
    api.add_resource(DeviceDelete, '/device/delete/<int:did>')
    api.add_resource(DeviceUpdate, '/device/update/<int:did>')
    api.add_resource(DeviceInfo, '/device/info/<int:did>')
    api.add_resource(DeviceData, '/device/data/<int:did>')
    
    # /data
    api.add_resource(DataYearList, '/device/dataYearList')
    api.add_resource(DataList, '/device/dataList')
