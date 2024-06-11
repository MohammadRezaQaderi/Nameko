from nameko.web.handlers import http
import grpc
import service1_pb2
import service1_pb2_grpc
import service2_pb2
import service2_pb2_grpc
import json

class GatewayService:
    name = "gateway_service"

    @http('POST', '/service1/some-function')
    def handle_service1_some_function(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.call_service1_some_function(data)
        return 200, json.dumps({'result': response.result})

    @http('POST', '/service1/insert-users')
    def handle_service1_insert_users(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.call_service1_insert_users(data)
        return 200, json.dumps({'result': response.result})

    @http('POST', '/service1/get-users-by-national-id')
    def handle_service1_get_users_by_national_id(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.call_service1_get_users_by_national_id(data)
        return 200, json.dumps({'users': [{'name': user.name, 'national_id': user.national_id, 'phone': user.phone, 'message': user.message} for user in response.users]})

    @http('POST', '/service2/another-function')
    def handle_service2_another_function(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.call_service2_another_function(data)
        return 200, json.dumps({'result': response.result})

    @http('POST', '/service2/insert-status')
    def handle_service2_insert_status(self, request):
        data = json.loads(request.get_data(as_text=True))
        response = self.call_service2_insert_status(data)
        return 200, json.dumps({'result': response.result})

    @http('GET', '/service2/get-status')
    def handle_service2_get_status(self, request):
        phone = request.args.get('phone')
        response = self.call_service2_get_status(phone)
        return 200, json.dumps({'status': response.status})

    def call_service1_some_function(self, data):
        with grpc.insecure_channel('service1:50051') as channel:
            stub = service1_pb2_grpc.Service1Stub(channel)
            grpc_request = service1_pb2.Request(parameter=data['parameter'])
            grpc_response = stub.SomeFunction(grpc_request)
            return grpc_response

    def call_service1_insert_users(self, data):
        with grpc.insecure_channel('service1:50051') as channel:
            stub = service1_pb2_grpc.Service1Stub(channel)
            users = [
                service1_pb2.User(name=user['name'], national_id=user['national_id'], phone=user['phone'])
                for user in data['users']
            ]
            grpc_request = service1_pb2.UserRequest(message=data['message'], users=users)
            grpc_response = stub.InsertUsers(grpc_request)
            return grpc_response

    def call_service1_get_users_by_national_id(self, data):
        with grpc.insecure_channel('service1:50051') as channel:
            stub = service1_pb2_grpc.Service1Stub(channel)
            grpc_request = service1_pb2.NationalIdRequest(national_id=data['national_id'])
            grpc_response = stub.GetUsersByNationalId(grpc_request)
            return grpc_response

    def call_service2_another_function(self, data):
        with grpc.insecure_channel('service2:50052') as channel:
            stub = service2_pb2_grpc.Service2Stub(channel)
            grpc_request = service2_pb2.Request(parameter=data['parameter'])
            grpc_response = stub.AnotherFunction(grpc_request)
            return grpc_response

    def call_service2_insert_status(self, data):
        with grpc.insecure_channel('service2:50052') as channel:
            stub = service2_pb2_grpc.Service2Stub(channel)
            grpc_request = service2_pb2.StatusRequest(phone=data['phone'], status=data['status'])
            grpc_response = stub.InsertStatus(grpc_request)
            return grpc_response

    def call_service2_get_status(self, phone):
        with grpc.insecure_channel('service2:50052') as channel:
            stub = service2_pb2_grpc.Service2Stub(channel)
            grpc_request = service2_pb2.StatusQuery(phone=phone)
            grpc_response = stub.GetStatus(grpc_request)
            return grpc_response
