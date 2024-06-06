from nameko.rpc import RpcProxy
from grpc_entrypoint import Grpc
import user_pb2
import user_pb2_grpc


class GatewayService(user_pb2_grpc.UserServiceServicer):
    name = "gateway"

    service1 = RpcProxy('microservice1')
    service2 = RpcProxy('microservice2')

    @Grpc
    def AddUserPhone(self, request, context):
        response = self.service1.add_user_phone(request.user_id, request.phone, request.status)
        return user_pb2.UserResponse(message=response, success=True)

    @Grpc
    def GetUserPhone(self, request, context):
        response = self.service1.get_user_phone(request.user_id)
        return user_pb2.UserResponse(message=response, success=True)

    @Grpc
    def AddUserPhone2(self, request, context):
        response = self.service2.add_user_phone(request.user_id, request.phone, request.status)
        return user_pb2.UserResponse(message=response, success=True)

    @Grpc
    def GetUserPhone2(self, request, context):
        response = self.service2.get_user_phone(request.user_id)
        return user_pb2.UserResponse(message=response, success=True)


grpc = Grpc.decorator
