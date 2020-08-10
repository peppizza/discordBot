FROM python:3
ENV PYTHONUNBUFFERED 1
ENV IS_IN_DOCKER Yes
RUN mkdir /code
WORKDIR /code
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile
COPY . /code/