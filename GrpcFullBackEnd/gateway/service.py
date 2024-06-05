from nameko.web.handlers import http
import grpc
from products_pb2 import ProductRequest
from products_pb2_grpc import ProductServiceStub


class GatewayService:
    name = "gateway_service"

    @http('GET', '/api/products/<int:product_id>')
    def get_product(self, request, product_id):
        with grpc.insecure_channel('product_service:50051') as channel:
            stub = ProductServiceStub(channel)
            response = stub.GetProduct(ProductRequest(product_id=product_id))
        return response.json()

    @http('GET', '/api/orders')
    def get_orders(self, request):
        # Logic to get orders from the gRPC service
        return jsonify({'orders': []})
