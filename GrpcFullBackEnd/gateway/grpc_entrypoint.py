from nameko.extensions import Entrypoint
from concurrent import futures
import grpc
import user_pb2_grpc


class GrpcEntrypoint(Entrypoint):
    def __init__(self, *args, **kwargs):
        self.servicer_cls = args[0]
        super(GrpcEntrypoint, self).__init__()

    def start(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        servicer = self.servicer_cls()
        user_pb2_grpc.add_UserServiceServicer_to_server(servicer, self.server)
        self.server.add_insecure_port('[::]:50051')
        self.server.start()

    def stop(self):
        self.server.stop(0)


grpc = GrpcEntrypoint.decorator
