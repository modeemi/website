# [Modeemi ry website](https://www.modeemi.fi)

[![Build Status](https://travis-ci.org/modeemi/website.svg?branch=master)](https://travis-ci.org/modeemi/website)
[![Coverage Status](https://codecov.io/gh/modeemi/website/branch/master/graph/badge.svg)](https://codecov.io/gh/imodeemi/website)
[![Updates](https://pyup.io/repos/github/modeemi/website/shield.svg)](https://pyup.io/repos/github/modeemi/website/)

Modeemi ry website for the Finnish IT club based on Tampere, Finland.

Built on top of Python, Django and PostgreSQL.

### Developing

This guide assumes you have some experience in Django development.

Development environment can be easily provisioned with virtualenv:

    python3 -m venv ~/.virtualenvs/modeemi
    source ~/.virtualenvs/modeemi/bin/activate
    pip install -r requirements.txt
    tox
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput
    python manage.py runserver

### Committing

Please run test suite before committing your changes:

    tox

If you have implemented new views or functionality, implement tests for those as well.

If you modify the views, remember to run `python manage.py makemigrations` before committing.

### Updating the running web service

The web service Docker container is automatically built by a Dockerhub job
from the `master` branch and a new version is deployed onto the web server periodically.

https://hub.docker.com/u/modeemi

To update the project you can

- Go get a soda and wait for 15 minutes for a cronjob to update the site.
- Manually run `sudo webupdate` on the web server.
