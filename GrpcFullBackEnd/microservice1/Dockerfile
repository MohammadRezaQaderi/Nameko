FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
COPY wait-for-it.sh .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y netcat

COPY microservice1/ ./microservice1/
COPY config.yml .


RUN chmod +x wait-for-it.sh

CMD ["./wait-for-it.sh", "service1_db", "5432", "--", "./wait-for-it.sh", "service1_redis", "6379", "--", "nameko", "run", "--config", "config.yml", "microservice1.service"]
