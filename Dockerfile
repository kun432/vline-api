FROM mcr.microsoft.com/devcontainers/python:0-3.10

RUN apt update -y \
    && apt install -y ruby locales \
    && sed -i '/^#.* ja_JP.UTF-8 /s/^#//' /etc/locale.gen \
    && locale-gen \
    && ln -fs /usr/share/zoneinfo/Asia/Tokyo /etc/localtime\
    && dpkg-reconfigure -f noninteractive tzdata
RUN apt install -y chromium chromium-driver
ENV LANG="ja_JP.UTF-8"
ENV LANGUAGE="ja_JP:ja"
ENV LC_ALL="ja_JP.UTF-8"

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
USER vscode

WORKDIR /tmp
COPY requirements.txt .

RUN pip install -r requirements.txt
