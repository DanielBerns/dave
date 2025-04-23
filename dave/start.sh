#!/usr/bin/env bash

. ~/.venvs/dave/bin/activate
flask db init
flask db migrate -m "Initial database migration."
flask db upgrade
deactivate
