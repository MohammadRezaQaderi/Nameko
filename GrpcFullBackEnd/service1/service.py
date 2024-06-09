from concurrent import futures
import grpc
import service1_pb2
import service1_pb2_grpc


class Service1(service1_pb2_grpc.Service1Servicer):
    def SomeFunction(self, request, context):
        response = service1_pb2.Response()
        response.result = "Processed service 1 " + request.parameter
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service1_pb2_grpc.add_Service1Servicer_to_server(Service1(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
