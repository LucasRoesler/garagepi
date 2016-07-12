FROM python:3

ENV PYTHONUNBUFFERED 1
RUN pip install -U pip


RUN mkdir -p /garage
COPY requirements.txt /garage/requirements.txt

RUN pip install --no-cache-dir -r /garage/requirements.txt

COPY ./api/ /garage/
WORKDIR /garage
