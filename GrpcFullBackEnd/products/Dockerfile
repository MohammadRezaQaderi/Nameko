FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN python -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. ./protos/products.proto

CMD ["nameko", "run", "--config", "config.yml", "service"]
