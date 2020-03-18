FROM python:3-alpine AS base

RUN apk update && apk add --no-cache build-base libffi-dev tzdata

RUN adduser -S datagenerator

COPY /datagenerator/requirements /requirements

WORKDIR /datagenerator

RUN pip config set global.index-url "https://pypi.python.org/simple"
RUN pip install dumb-init==1.2.2
RUN pip install -r /requirements/main.txt

FROM base as app
COPY datasets /datasets
COPY datagenerator/app /app

FROM app AS release

ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

FROM release AS dev-base
RUN apk add --no-cache bash

FROM dev-base As local
USER datagenerator
CMD ["tail", "-f", "/dev/null"]

FROM dev-base as test-base
USER datagenerator
RUN pip install -r /requirements/test.txt --no-deps
CMD ["pytest"]
