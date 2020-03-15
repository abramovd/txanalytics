FROM python:3-alpine AS base

RUN apk update && apk add --no-cache build-base tzdata

RUN adduser -S tx_api

COPY /requirements/api /tx_api/requirements

WORKDIR /tx_api

RUN pip config set global.index-url "https://pypi.python.org/simple"
RUN pip install dumb-init==1.2.2
RUN pip install -r /tx_api/requirements/main.txt

FROM base as app
COPY api /tx_api/app

FROM app AS release

ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

EXPOSE 8000

FROM release AS dev-base
RUN apk add --no-cache bash

FROM dev-base As local
USER tx_api
CMD ["uvicorn", "app.main:app", "--reload", "--host=0.0.0.0", "--port=8000"]

FROM dev-base as test-base
USER tx_api
RUN pip install -r /tx_api/requirements/test.txt --no-deps
CMD ["pytest"]

