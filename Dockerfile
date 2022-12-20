FROM python:3.8-buster

COPY . /Camera

RUN python3 -m pip install -U pip
RUN python3 -m pip install -r /Camera/requirements.txt
RUN /bin/sh -c 'cd /Camera; python3 Setup.py'