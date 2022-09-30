FROM python:3.9-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY . /code/

RUN pip install --upgrade pip
RUN pip install --upgrade -r requirements.txt
