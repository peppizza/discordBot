FROM python:3

WORKDIR /usr/src/app

ENV IS_IN_DOCKER Yes

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./fellow_kids.py" ]
