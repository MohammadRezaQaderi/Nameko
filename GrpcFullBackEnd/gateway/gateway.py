from nameko.web.handlers import http
import grpc
import service1_pb2
import service1_pb2_grpc
import service2_pb2
import service2_pb2_grpc
import json


class GatewayService:
    name = "gateway_service"

    @http('POST', '/service1')
    def handle_service1(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.call_service1(data)
        return 200, json.dumps({'result': response.result})

    @http('POST', '/service2')
    def handle_service2(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.call_service2(data)
        return 200, json.dumps({'result': response.result})

    def call_service1(self, data):
        with grpc.insecure_channel('service1:50051') as channel:
            stub = service1_pb2_grpc.Service1Stub(channel)
            grpc_request = service1_pb2.Request(parameter=data['parameter'])
            grpc_response = stub.SomeFunction(grpc_request)
            return grpc_response

    def call_service2(self, data):
        with grpc.insecure_channel('service2:50052') as channel:
            stub = service2_pb2_grpc.Service2Stub(channel)
            grpc_request = service2_pb2.Request(parameter=data['parameter'])
            grpc_response = stub.AnotherFunction(grpc_request)
            return grpc_response
