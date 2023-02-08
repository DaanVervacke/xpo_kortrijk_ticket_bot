FROM python:latest

WORKDIR /usr/src/app

COPY . .

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install --no-cache-dir -r requirements.txt --upgrade pip

CMD python bot.py