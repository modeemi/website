#!/bin/bash

# Initialize environment and run unit tests

set -xe

cd "$(realpath "$0/..")"

echo 'Testing Bower requirements installation'
bower install

if [[ ! -d virtualenv ]]; then
    echo 'Creating virtualenv'
    virtualenv virtualenv
fi

source virtualenv/bin/activate

echo 'Testing Python requirements installation'
pip install -r requirements.txt
echo 'Running Python and Django unit tests'
python manage.py test

