FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

RUN useradd -ms /bin/bash myuser

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /scraper

USER myuser

COPY requirements.txt /scraper

RUN pip install --no-cache-dir -r requirements.txt

COPY . /scraper

ENV PATH="/home/myuser/.local/bin:${PATH}"




