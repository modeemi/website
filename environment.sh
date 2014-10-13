#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

if [[ ! -d virtualenv ]]; then
    virtualenv virtualenv
fi

source virtualenv/bin/activate &&
    pip install -r requirements.txt &&
    bower install &&
    python manage.py migrate
    python manage.py loaddata modeemintternet/fixtures/initial.json
