FROM ubuntu:20.04

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone

RUN apt update
RUN apt install -y -q build-essential gcc g++ python3 python3-pip openjdk-11-jdk-headless libssl-dev
RUN python3 -m pip install tqdm
COPY . /work
