FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /scraper

COPY requirements.txt /scraper

RUN pip install --no-cache-dir -r requirements.txt

COPY . /scraper





