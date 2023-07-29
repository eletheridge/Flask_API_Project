# start with a base image
# FROM ubuntu:16.04
FROM python:3.11-slim

# set environment vars
ENV FLASK_APP="/app/app.py"
ENV FLASK_ENV="development"
ENV AUTH_HEADER_KEY="34f1f529f2fe86fd5d29f4a8feb7f3860a3a4568fdbdd1186dd659282553bf1f"

USER root

# install dependencies
RUN apt-get update && apt-get install -y \
apt-utils \
nginx \
git \
python3-pip

RUN echo "America/New_York" > /etc/timezone; dpkg-reconfigure -f noninteractive tzdata

RUN pip install --upgrade pip

ADD ./requirements.txt ./app/requirements.txt
RUN pip3 install -r /app/requirements.txt

EXPOSE 5432