rm -rf logs
mkdir logs

cd backend
. .venv/bin/activate
nohup .venv/bin/python app.py > ../logs/backend.log 2>&1 &
deactivate
cd ..
echo "Backend started"

cd frontend
nohup npm run dev > ../logs/frontend.log 2>&1 &
cd ..
echo "Frontend started"

cd server
. .venv/bin/activate
nohup .venv/bin/python server.py > ../logs/server.log 2>&1 &
nohup .venv/bin/python mock/sensor.py > ../logs/sensor.log 2>&1 &
nohup .venv/bin/python mock/actuator.py > ../logs/actuator.log 2>&1 &
deactivate
cd ..
