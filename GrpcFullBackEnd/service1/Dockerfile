FROM python:3.8-slim

WORKDIR /app
COPY . /app
COPY ../protos /app/protos

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Generate gRPC code
RUN python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/service1.proto
RUN python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/service2.proto

CMD ["python", "service.py"]
