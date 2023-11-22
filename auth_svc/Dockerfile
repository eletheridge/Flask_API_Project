# start with a base image
# FROM ubuntu:16.04
FROM python:3.11-slim

# set environment vars
ENV FLASK_APP="/app/app.py"
ENV FLASK_ENV="development"

USER root

# install dependencies
RUN apt-get update && apt-get install -y \
apt-utils \
nginx \
git \
python3-pip

RUN echo "America/New_York" > /etc/timezone; dpkg-reconfigure -f noninteractive tzdata

RUN pip install --upgrade pip

ADD requirements.txt ./app/requirements.txt
RUN pip3 install -r /app/requirements.txt

EXPOSE 5433

WORKDIR /app
ENTRYPOINT ["./launch.sh"]