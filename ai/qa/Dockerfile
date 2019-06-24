FROM nvidia/cuda:9.0-base

RUN apt-get -y update
RUN apt-get -y upgrade
# RUN apt-get install -y software-properties-common
# RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get -y install python3-pip
# RUN apt-get install python3.6

WORKDIR /usr/src/app

RUN pip3 install pipenv

COPY . .

WORKDIR /usr/src/app/pytorch
RUN     export LC_ALL=C.UTF-8 && export LANG=C.UTF-8 && pipenv install

CMD pipenv run python server.py
