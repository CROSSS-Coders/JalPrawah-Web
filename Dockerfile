FROM python:3.7-alpine

WORKDIR /code

ENV FLASK_APP app/app.py

ENV FLASK_RUN_HOST 0.0.0.0

RUN apk add --no-cache gcc musl-dev linux-headers tzdata libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 

RUN apk add --no-cache mariadb-connector-c-dev ;\
    apk add --no-cache --virtual .build-deps \
        build-base \
        mariadb-dev ;\
    pip install mysqlclient;\
    apk del .build-deps 

RUN ls /usr/share/zoneinfo

RUN cp /usr/share/zoneinfo/Asia/Kolkata /etc/localtime

RUN echo "Asia/Kolkata" >  /etc/timezone

RUN apk del tzdata

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# COPY . .

CMD ["flask", "run"]