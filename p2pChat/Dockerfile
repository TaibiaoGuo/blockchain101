FROM python:3
# STEP1: test
# If test faild, docker building process would faild too.
# The test container will be auto removed when build successed.
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Install Python test tool pytest
RUN pip install --no-cache-dir pytest pytest-asyncio
COPY . .
RUN pytest


FROM python:3
# STEP2: build images
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Owner infomations:
# github.com/TaibiaoGuo/blockchain101@experiment
MAINTAINER Taibiao Guo
# Server Side
EXPOSE 12467/tcp
EXPOSE 12467/udp
# Client Side
EXPOSE 12468/tcp
EXPOSE 12468/udp
CMD [ "python", "./p2pChat.py" ]
