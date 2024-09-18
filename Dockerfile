FROM python:3.12.6-alpine3.20

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN apk update \
    && apk add gcc python3-dev musl-dev \
    && apk add nano bash htop \
    && apk add zlib-dev jpeg-dev

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# COPY .bashrc /root/
