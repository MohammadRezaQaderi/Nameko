FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. products.proto
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. orders.proto

CMD ["python", "gateway.py"]
