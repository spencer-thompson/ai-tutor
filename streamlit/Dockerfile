# FROM python:latest
FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python util.py

EXPOSE 8501
