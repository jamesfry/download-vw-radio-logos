FROM python:3.8-slim-buster

RUN apt-get update -y && pip3 install pipenv

ENV USER python
ENV HOME /home/$USER

RUN useradd -m $USER && echo $USER:$USER | chpasswd && adduser $USER sudo
RUN chown $USER:$USER $HOME
RUN mkdir /logos && chown $USER:$USER /logos

USER $USER

ADD . /app

WORKDIR /app

RUN pipenv install

VOLUME /logos

CMD [ "pipenv", "run", "download"]
