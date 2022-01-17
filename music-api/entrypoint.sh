#!/bin/sh

flask db init
flask db migrate
flask db upgrade
flask run --port 5555 --host 0.0.0.0