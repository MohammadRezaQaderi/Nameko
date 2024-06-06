FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
COPY wait-for-it.sh .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y netcat

COPY . .
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto


RUN chmod +x wait-for-it.sh

CMD ["./wait-for-it.sh", "rabbitmq", "5672", "--", "./wait-for-it.sh", "service1", "8001", "--", "./wait-for-it.sh", "service2", "8002", "--", "nameko", "run", "--config", "config.yml", "gateway"]
