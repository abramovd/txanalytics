FROM python:3-alpine AS base

RUN apk update && apk add --no-cache build-base tzdata

RUN adduser -S api

COPY /api/requirements /requirements

WORKDIR /api

RUN pip config set global.index-url "https://pypi.python.org/simple"
RUN pip install dumb-init==1.2.2
RUN pip install -r /requirements/main.txt

FROM base as app
COPY datasets /datasets
COPY api/app /app

FROM app AS release

ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

EXPOSE 8000

FROM release AS dev-base
RUN apk add --no-cache bash

FROM dev-base As local
USER api
CMD ["uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=8000"]

FROM dev-base as test-base
USER api
RUN pip install -r /requirements/test.txt --no-deps
CMD ["pytest"]

