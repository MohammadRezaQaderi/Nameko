from nameko_grpc.entrypoint import Grpc
from service1_pb2 import Product, Products, ProductId, Empty
from service1_pb2_grpc import ProductsStub
from nameko.events import event_handler
from products import dependencies

grpc = Grpc.implementing(ProductsStub)


class ProductsService:
    name = "products"

    storage = dependencies.Storage()

    @grpc
    def CreateProduct(self, request, context):
        self.storage.create({
            "id": request.id,
            "title": request.title,
            "passenger_capacity": request.passenger_capacity,
            "maximum_speed": request.maximum_speed,
            "in_stock": request.in_stock,
        })
        return request

    @grpc
    def GetProduct(self, request, context):
        product_id = request.id
        product = self.storage.get(product_id)
        return Product(**product)

    @grpc
    def ListProducts(self, request, context):
        products = self.storage.list()
        return Products(products=[Product(**product) for product in products])

    @event_handler("orders", "order_created")
    def handle_order_created(self, payload):
        for product in payload["order"]["order_details"]:
            self.storage.decrement_stock(product["product_id"], product["quantity"])
