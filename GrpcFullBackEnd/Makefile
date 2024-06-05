.PHONY: install-dependencies develop build-images deploy-services clean

install-dependencies:
    pip install --upgrade pip setuptools wheel
    pip install -r gateway/requirements.txt --verbose
    pip install -r products/requirements.txt --verbose

develop:
    docker-compose up --build

build-images:
    docker build -t gateway:latest ./gateway
    docker build -t products:latest ./products

deploy-services:
    kubectl apply -f k8s

clean:
    docker-compose down -v --rmi all
    find . -type d -name "__pycache__" -exec rm -r {} +
    find . -type d -name ".pytest_cache" -exec rm -r {} +
    find . -type f -name "*.pyc" -exec rm -r {} +
