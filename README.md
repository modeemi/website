# [Modeemi ry website](https://www.modeemi.fi)

[![Build](https://github.com/modeemi/website/workflows/Build/badge.svg)](https://github.com/modeemi/website/actions)
[![Coverage](https://codecov.io/gh/modeemi/website/branch/master/graph/badge.svg)](https://codecov.io/gh/imodeemi/website)

Modeemi ry website for the Finnish IT club based on Tampere, Finland.

Built on top of Python 3.10, Django 4.0 and PostgreSQL.

### Developing

This guide assumes you have some experience in Django development.

Setting up postgresql:

    # Create dev environment user and database
    CREATE USER modeemintternet PASSWORD 'modeemintternet' CREATEDB;
    CREATE DATABASE modeemiuserdb WITH OWNER = modeemintternet;

Development environment can be easily provisioned with virtualenv:

    # Provision a virtualenv
    python -m venv .venv/
    source .venv/bin/activate

    # Install development requirements
    python -m pip install --upgrade pip
    python -m pip install --upgrade pip-tools
    python -m pip install -r requirements.txt

    # Run tox QA test setup
    python -m tox

    # Prepare and run the development server
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput
    python manage.py runserver

### Committing

Please run test suite before committing your changes:

    python -m tox

If you have implemented new views or functionality, implement tests for those as well.

If you modify the views, remember to run `python manage.py makemigrations` before committing.

### Updating versions

Python version can be upgraded by changing the Python version tag in the following locations:

- `Dockerfile`
- `mypy.ini`
- `pyproject.toml`
- `.github/workflows/build.yml`

You can update all Python package versions by updating `requirements.in` and then running:

    pip-compile -U

This compiles a new `requirements.txt` file with versions pinned, locking the development as well as production runtime environments.

Afterwards commit the changes and a new image will be built.

### Updating the running web service

The web service Docker container is automatically built from the `master` branch. Newest release of the container is hosted with GitHub Packages.

https://github.com/modeemi/website/pkgs/container/website

After code is pushed, a CI job will automatically run tests and linters and build the containter. To pull the container into production you can:

- Go get a soda and wait for 15 minutes for a cronjob to update the site OR
- Manually run `sudo webupdate` on the web server.

