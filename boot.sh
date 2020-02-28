#!/bin/sh
source venv/bin/activate
flask resetdb
flask add_toydata
flask run --host="0.0.0.0"
# exec gunicorn -b :5000 --access-logfile - --error-logfile - shield_api:app
