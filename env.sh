# backend
cd backend
python3 -m venv .venv
. .venv/bin/activate
.venv/bin/pip install -r requirements.txt
deactivate
cd ..

# mqtt
cd ../mqtt
python3 -m venv .venv
. .venv/bin/activate
.venv/bin/pip install -r requirements.txt
deactivate
cd ..