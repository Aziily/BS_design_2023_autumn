<div align='center'><img src="./assets/logo.png"></div>

# ZJU B/S Design 2023 autumn

## Summary

This is the project for the assignment of ZJU BS Design in 2023 autumn-winter term



## Quick Start

### Docker

Docker image is on the way

### Local

1. Run `env.sh` to prepare environment for all service

2. Different serivce

   1. Backend: this is the backend for console

      ```shell
      cd backend
      . .venv/bin/activate
      .venv/bin/python app.py
      ```

   2. Frontend: this is the frontend for console

      ```shell
      cd frontend
      npm run dev
      ```

   3. Server: this is the mqtt server

      ```shell
      cd server
      . .venv/bin/activate
      .venv/bin/python server.py
      
      # if need mock, run below
      .venv/bin/python mock/sensor.py
      .venv/bin/python mock/actuator.py
      ```

3. By default, backend is running on `:5000`, frontend is running on `:9528`, server is depending on `broker.emqx.io:1883`

4. Use `localhost:9528` to see the panel



## Organization

- `assets` - assets for the project
- `backend` - backend code for console, using `python` with frame `flask`
- `frontend`- frontend code for console, using `vue2` with frame `vue-element-admin`
- `server` - server code for mqtt, using `python`



## Inference

* **Frontend**
  * [vue-element-admin (panjiachen.github.io)](https://panjiachen.github.io/vue-element-admin-site/#/)
  * [Element - A Desktop UI Toolkit for Web](https://element.eleme.cn/#/en-US)
  * [组件 | vue-amap (guyixi.cn)](https://docs.guyixi.cn/vue-amap/#/)
  * [概述-地图 JS API | 高德地图API (amap.com)](https://lbs.amap.com/api/javascript-api/summary)
* **Backend**
  * [Flask 中文网 (github.net.cn)](https://flask.github.net.cn/)
    * [Flask-SQLAlchemy — Flask-SQLAlchemy Documentation (3.1.x) (palletsprojects.com)](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
    * [Flask-RESTful — Flask-RESTful 0.3.10 documentation](https://flask-restful.readthedocs.io/en/latest/index.html)
    * [Flask-JWT-Extended’s Documentation — flask-jwt-extended 4.5.3 documentation](https://flask-jwt-extended.readthedocs.io/en/stable/index.html)
* **Server**
  * [paho-mqtt · PyPI](https://pypi.org/project/paho-mqtt/)
  * [The Free Global Public MQTT Broker | Try Now | EMQ (emqx.com)](https://www.emqx.com/en/mqtt/public-mqtt5-broker)



## Other

Th backend api doc can be seen in `localhost:5000/apidocs`
