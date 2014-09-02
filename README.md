LRN2Django
==========

Python packages

    apt-get install python python-pip python-virtualenv nodejs

LDAP packages

    apt-get install python-dev libldap2-dev libsasl2-dev libssl-dev

pip packages

    source virtualenv/bin/activate
    pip install -r requirements.txt

bower packages

    bower install

Sync and migrate DB, collect static files

    python manage.py syncdb
    python manage.py migrate --auto
    python manage.py collectstatic
