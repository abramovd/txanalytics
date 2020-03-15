FROM python:3-alpine AS base

RUN apk update && apk add --no-cache build-base tzdata

RUN adduser -S tx_datagenerator

COPY /requirements/datagenerator /tx_datagenerator/requirements

WORKDIR /datagenerator

RUN pip config set global.index-url "https://pypi.python.org/simple"
RUN pip install setuptools --upgrade
RUN pip install dumb-init==1.2.2
RUN pip install -r /tx_datagenerator/requirements/main.txt

FROM base as app
COPY datagenerator /tx_datagenerator/app

FROM app AS release

ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

EXPOSE 8000

FROM release AS dev-base
RUN apk add --no-cache bash

FROM dev-base As local
USER tx_datagenerator
CMD ["tail", "-f", "/dev/null"]

FROM dev-base as test-base
USER tx_datagenerator
RUN pip install -r /tx_datagenerator/requirements/test.txt --no-deps
CMD ["pytest"]
