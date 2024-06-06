FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
COPY wait-for-it.sh .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y netcat

COPY microservice2/ ./microservice2/
COPY config.yml .
RUN chmod +x wait-for-it.sh

CMD ["./wait-for-it.sh", "service2_db", "5432", "--", "./wait-for-it.sh", "service2_redis", "6379", "--", "nameko", "run", "--config", "config.yml", "microservice2.service"]
