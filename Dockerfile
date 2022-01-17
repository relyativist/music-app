FROM python:3.7-alpine

WORKDIR /srv

RUN mkdir -p /srv/templates

ADD ./music-api/templates /srv/templates

COPY ./music-api/app.py ./music-api/entrypoint.sh ./music-api/requirements.txt /srv/

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN export FLASK_APP=/srv/app.py

RUN chmod +x /srv/entrypoint.sh

EXPOSE 5555

ENTRYPOINT [ "/bin/sh", "entrypoint.sh" ]


