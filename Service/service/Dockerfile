# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/service

CMD ["nameko", "run", "--config", "./config.yaml", "service1"]
