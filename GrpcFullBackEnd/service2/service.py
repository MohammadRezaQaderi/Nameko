from concurrent import futures
import grpc
import service2_pb2
import service2_pb2_grpc
import service1_pb2
import service1_pb2_grpc


class Service2(service2_pb2_grpc.Service2Servicer):
    def AnotherFunction(self, request, context):
        # Make a request to Service1
        with grpc.insecure_channel('service1:50051') as channel:
            stub = service1_pb2_grpc.Service1Stub(channel)
            service1_response = stub.SomeFunction(service1_pb2.Request(parameter=request.parameter))

        response = service2_pb2.Response()
        response.result = "Processed service2 " + request.parameter + " and got response: " + service1_response.result
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service2_pb2_grpc.add_Service2Servicer_to_server(Service2(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
