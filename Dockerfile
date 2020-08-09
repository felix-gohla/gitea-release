FROM python:3.8.5-alpine3.12

RUN pip3 install giteapy

COPY check.py /opt/resource/check
COPY in.py /opt/resource/in
COPY out.py /opt/resource/out

