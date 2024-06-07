import grpc
from concurrent import futures

from service1_pb2_grpc import ProductsStub
from service1_pb2 import Product, ProductId, Empty, Products

from service2_pb2_grpc import OrdersStub
from service2_pb2 import Order, OrderResponse


class GatewayService:

    def __init__(self):
        self.products_channel = grpc.insecure_channel('service1:50051')
        self.products_stub = ProductsStub(self.products_channel)

        self.orders_channel = grpc.insecure_channel('service2:50052')
        self.orders_stub = OrdersStub(self.orders_channel)

    def create_product(self, product_data):
        product = Product(**product_data)
        response = self.products_stub.CreateProduct(product)
        return response

    def get_product(self, product_id):
        product_id_message = ProductId(id=product_id)
        response = self.products_stub.GetProduct(product_id_message)
        return response

    def list_products(self):
        empty_message = Empty()
        response = self.products_stub.ListProducts(empty_message)
        return response

    def create_order(self, order_data):
        order = Order(**order_data)
        response = self.orders_stub.CreateOrder(order)
        return response


if __name__ == "__main__":
    gateway_service = GatewayService()
    # Example usage:
    product_data = {
        "id": "1",
        "title": "Test Product",
        "passenger_capacity": 4,
        "maximum_speed": 200,
        "in_stock": True
    }
    print(gateway_service.create_product(product_data))

    product_id = "1"
    print(gateway_service.get_product(product_id))

    print(gateway_service.list_products())

    order_data = {
        "id": "1",
        "order_details": [
            {"product_id": "1", "quantity": 2}
        ]
    }
    print(gateway_service.create_order(order_data))
