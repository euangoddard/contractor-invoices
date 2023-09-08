FROM python:3.11-slim

WORKDIR /opt/ci

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/opt/ci