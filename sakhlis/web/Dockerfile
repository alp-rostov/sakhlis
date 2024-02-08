FROM python:3.11-slim

RUN mkdir web

WORKDIR web

ADD requirements.txt /web/

RUN pip install -r requirements.txt

ADD . /web/

CMD gunicorn web.wsgi:application -b 0.0.0.0:8000