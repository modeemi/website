# [Modeemi ry website](https://www.modeemi.fi)

[![Requirements Status](https://requires.io/github/aleksih/modeemintternet/requirements.svg?branch=master)](https://requires.io/github/aleksih/modeemintternet/requirements/?branch=master) [![Build Status](https://travis-ci.org/aleksih/modeemintternet.svg?branch=master)](https://travis-ci.org/aleksih/modeemintternet)

### Prelude

Modeemi ry website for the Finnish IT club based on Tampere, Finland.

Built on top of Python 2, Django and PostgreSQL.

_tl;dr: Intternet 2.x_

### Developing

This guide assumes you have some experience in Django development and doesn't have 100% coverage. 

You can find plenty of tutorials on the Intternets describing the specifics of Django and assorted plugins.

Install apt and npm packages

    apt-get install python python-dev python-pip python-virtualenv \
        nodejs nodejs-legacy npm libpq-dev libldap2-dev libsasl2-dev libssl-dev
    npm i -g bower

Create an user for hosting and add the required file system structures

    adduser modeemintternet -d /opt/intternet/
    mkdir /var/www/modeemintternet
    chown -R modeemintternet:modeemintternet /var/www/modeemintternet
    chmod 775 /var/www/modeemintternet

Log in as the correct user, get source and create a virtualenv for the project

    su - modeemintternet
    git clone https://github.com/aleksih/modeemintternet.git
    cd modeemintternet
    virtualenv virtualenv
    source virtualenv/bin/activate
    pip install -r requirements.txt
    bower install

Create, sync and migrate the DB, if you're using PostgreSQL configure credentials in `settings.py`.

    # first create the database as root as per settings.py credentials
    python manage.py migrate

For production, remember to collect static files and install fixtures:

    python manage.py collectstatic
    python manage.py loaddata modeemintternet/fixtures/initial.json

Copy the configurations for the service (as root), use respective directory names

    cp etc/... /etc/...

Configure the secret keys in `/etc/modeemintternet` for something unique (generated preferably).

Restart the services for the changes to take effect

    service supervisor restart
    service apache2 restart

That's about it.
