# [Modeemi ry website](https://www.modeemi.fi)

[![Build Status](https://travis-ci.org/modeemi/intternetvelho.svg?branch=master)](https://travis-ci.org/modeemi/intternetvelho)
[![Coverage Status](https://coveralls.io/repos/modeemi/intternetvelho/badge.svg?branch=master)](https://coveralls.io/r/modeemi/intternetvelho?branch=master)
[![Updates](https://pyup.io/repos/github/modeemi/intternetvelho/shield.svg)](https://pyup.io/repos/github/modeemi/intternetvelho/)

Modeemi ry website for the Finnish IT club based on Tampere, Finland.

Built on top of Python, Django and PostgreSQL.

### Developing

This guide assumes you have some experience in Django development.

Development environment can be easily provisioned with Vagrant:

    vagrant up
    vagrant ssh
    cd /vagrant
    source ./virtualenv/bin/activate
    python -Wall manage.py test
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput
    python manage.py runserver

### Committing

Please run test suite before committing your changes.

    # activate the environment as described before
    python manage.py test
    prospector

If you have implemented new views or functionality, implement tests for those as well.

If you modify the views, remember to run `python manage.py makemigrations` before committing.

### Updating the running web service

The web service Docker container is automatically built by a Dockerhub job
from the `master` branch and a new version is deployed onto the web server periodically.

To update the project you can

- Go get a soda and wait for 15 minutes for a cronjob to update the site.
- Manually run `webupdate` on the web server as `root`.
