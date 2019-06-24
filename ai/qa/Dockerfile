FROM python:3.6

WORKDIR /usr/src/app

RUN pip install pipenv

COPY . .

WORKDIR /usr/src/app/pytorch
RUN pipenv install

CMD pipenv run python server.py
