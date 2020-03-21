FROM python:3.7-alpine AS base

RUN apk update && apk add --no-cache build-base tzdata libffi-dev libxml2-dev libxslt-dev

RUN adduser -S notebook

COPY /notebook/requirements /requirements

WORKDIR /notebook

RUN pip config set global.index-url "https://pypi.python.org/simple"
RUN pip install dumb-init==1.2.2

# For matlotlib
RUN pip install cython==0.29.15

RUN pip install -r /requirements/main.txt

FROM base as app
COPY notebook/work /work

FROM app AS release

ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/work

EXPOSE 8888

FROM release AS dev-base
RUN apk add --no-cache bash

FROM dev-base As local
USER notebook
CMD ["jupyter", "notebook"]
