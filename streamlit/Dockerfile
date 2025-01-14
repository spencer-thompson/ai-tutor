# FROM python:latest
FROM python:3.12

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt --upgrade

COPY . .

RUN python util.py

EXPOSE 8501
