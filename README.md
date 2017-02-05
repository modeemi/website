# [Modeemi ry website](https://www.modeemi.fi)

[![Build Status](https://travis-ci.org/modeemi/intternetvelho.svg?branch=master)](https://travis-ci.org/modeemi/intternetvelho)
[![Coverage Status](https://coveralls.io/repos/modeemi/intternetvelho/badge.svg?branch=master)](https://coveralls.io/r/modeemi/intternetvelho?branch=master)
[![Requirements Status](https://requires.io/github/modeemi/intternetvelho/requirements.svg?branch=master)](https://requires.io/github/modeemi/intternetvelho/requirements/?branch=master)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/0eee6dbb748f474196c63d03575a8d63/badge.svg)](https://www.quantifiedcode.com/app/project/0eee6dbb748f474196c63d03575a8d63)

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

### Updating the running web service

To update the project you can

- Go get a soda and wait for a maximum of two hours for a cronjob to update the site.
- Manually run `webupdate` on the web server as `root`.
