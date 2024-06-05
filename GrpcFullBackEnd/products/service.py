from nameko.rpc import rpc
from nameko_grpc.entrypoint import Grpc
from products_pb2 import ProductResponse, ProductRequest
from products_pb2_grpc import ProductServiceServicer, add_ProductServiceServicer_to_server

grpc = Grpc.implementing(ProductServiceServicer)


class ProductService:
    name = "product_service"

    @rpc
    def get_product(self, product_id):
        # Dummy product data
        product = {"id": product_id, "name": "Sample Product", "price": 100}
        return product

    @grpc
    def GetProduct(self, request, context):
        product_id = request.product_id
        product = self.get_product(product_id)
        return ProductResponse(id=product['id'], name=product['name'], price=product['price'])
