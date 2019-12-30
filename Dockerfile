FROM python:3.8

EXPOSE 8888

ENV DJANGO_SETTINGS_MODULE="config.settings.docker"

ARG DJANGO_SECRET_KEY="notneededforbuilds"
ARG DATABASE_URL="postgres://not@neededforbuilds"
ARG RECAPTCHA_PUBLIC_KEY="notneededforbuilds"
ARG RECAPTCHA_PRIVATE_KEY="notneededforbuilds"

COPY scripts/entrypoint /usr/local/bin/entrypoint
RUN chmod a+x /usr/local/bin/entrypoint

WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

ADD . /app/

RUN python manage.py collectstatic --noinput

RUN groupadd -g 1001 modeemintternet
RUN useradd -u 1001 -g 1001 -d /app modeemintternet
USER modeemintternet

ENTRYPOINT ["/usr/local/bin/entrypoint"]
CMD [ \
  "gunicorn", \
  "--name", \
  "modeemintternet", \
  "--access-logfile", \
  "-", \
  "--access-logform", \
  "%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s '%(f)s' '%(a)s'", \
  "--log-level", \
  "info", \
  "--workers", \
  "2", \
  "--bind", \
  "0.0.0.0:8888", \
  "config.wsgi:application" \
]

ARG RELEASE
ENV RELEASE=${RELEASE}
