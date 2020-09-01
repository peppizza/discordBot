FROM python:3

ENV PYTHONUNBUFFERED 1
ENV IS_IN_DOCKER Yes
RUN mkdir /code

WORKDIR /code

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv

RUN echo "deb http://deb.debian.org/debian buster main contrib non-free" | tee /etc/apt/sources.list
RUN apt update

RUN apt -y install postgresql-client

RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections
RUN apt -y --no-install-recommends install ttf-mscorefonts-installer
RUN pipenv install --deploy --ignore-pipfile

COPY . /code/