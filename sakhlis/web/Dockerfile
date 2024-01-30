FROM python:3.11-slim

RUN mkdir web

WORKDIR web

ADD . /web/


RUN pip install -r requirements.txt

CMD gunicorn web.wsgi:application -b 0.0.0.0:8000