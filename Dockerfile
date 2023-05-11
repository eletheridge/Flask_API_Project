# start with a base image
# FROM ubuntu:16.04
FROM python:3.7-slim

# set environment vars
ENV FLASK_ENV=development

USER root

# install dependencies
RUN apt-get update && apt-get install -y \
apt-utils \
nginx \
git \
python3-pip

RUN echo "America/New_York" > /etc/timezone; dpkg-reconfigure -f noninteractive tzdata

RUN pip install --upgrade pip

#ADD ./app.py ./app.py
ADD ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

#ADD ./config /config

# -- configure ssh keys
RUN bash /config/deploy_keys/configure/ssh.sh /config/deploy_keys
RUN bash /config/deploy_keys/configure/requirements.sh /config



EXPOSE 5432