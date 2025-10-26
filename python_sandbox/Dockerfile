FROM python:3.13

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install uv

ENV PATH="/root/.local/bin:${PATH}"

COPY . .

EXPOSE 8081
