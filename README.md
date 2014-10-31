modeemintternet - Modeemi ry website
====================================

## Developing

Install apt packages

    apt-get install python python-dev python-pip python-virtualenv \
        nodejs nodejs-legacy libpq-dev libldap2-dev libsasl2-dev libssl-dev

Install pip packages

    source virtualenv/bin/activate
    pip install -r requirements.txt

Install bower packages

    bower install

Sync and migrate DB, if you're using PostgreSQL check `settings.py`.

    python manage.py syncdb
    python manage.py migrate

For production, remember to collect static files and install fixtures:

    python manage.py collectstatic
    python manage.py loaddata modeemintternet/fixtures/initial.json
