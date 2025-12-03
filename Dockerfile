from python:3.11.3-slim-bullseye

workdir /docker-app

copy requirements.txt .
run python -m pip install -r requirements.txt
copy . /docker-app
cmd flask --app accounting_app run -h 0.0.0.0 -p $PORT
