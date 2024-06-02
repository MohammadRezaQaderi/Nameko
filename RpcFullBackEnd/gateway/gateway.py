import json
from nameko.rpc import RpcProxy
from nameko.web.handlers import http


class GatewayService:
    name = 'gateway'

    service1_rpc = RpcProxy('service1')
    service2_rpc = RpcProxy('service2')

    @http('POST', '/create/service1')
    def create_service1(self, request):
        data = json.loads(request.get_data(as_text=True))
        result = self.service1_rpc.create(data)
        return json.dumps(result)

    @http('POST', '/create/service2')
    def create_service2(self, request):
        data = json.loads(request.get_data(as_text=True))
        result = self.service2_rpc.create(data)
        return json.dumps(result)

    @http('GET', '/hello/service1/<string:phone>')
    def hello_service1(self, request, phone):
        result = self.service1_rpc.hello(phone)
        return json.dumps(result)

    @http('GET', '/hello/service2/<string:phone>')
    def hello_service2(self, request, phone):
        result = self.service2_rpc.hello(phone)
        return json.dumps(result)
