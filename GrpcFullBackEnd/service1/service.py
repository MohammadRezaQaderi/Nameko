import psycopg2
import redis, time
from concurrent import futures
import grpc
import service1_pb2
import service1_pb2_grpc
import service2_pb2
import service2_pb2_grpc


class Service1(service1_pb2_grpc.Service1Servicer):
    def __init__(self):
        self.db_conn = self.connect_to_database()
        self.redis_conn = redis.StrictRedis(host='service2_redis', port=6379, db=0)
        self.create_table()

    def connect_to_database(self):
        max_retries = 5
        for _ in range(max_retries):
            try:
                return psycopg2.connect(
                    "dbname=service2_db user=service2_user password=service2_pass host=service2_db")
            except psycopg2.OperationalError:
                time.sleep(5)  # Wait for 5 seconds before retrying
        raise Exception("Could not connect to the database after several attempts")

    def create_table(self):
        create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(40),
        phone VARCHAR(12)
    );
    """
        with self.db_conn.cursor() as cursor:
            cursor.execute(create_table_query)
            self.db_conn.commit()

    def SomeFunction(self, request, context):
        response = service1_pb2.Response()
        response.result = "Processed " + request.parameter
        return response

    def InsertUsers(self, request, context):
        with self.db_conn.cursor() as cursor:
            for user in request.users:
                cursor.execute("INSERT INTO users (id, name, phone) VALUES (%s, %s, %s)",
                               (user.id, user.name, user.phone))
                # Call Service2's InsertStatus method
                with grpc.insecure_channel('service2:50052') as channel:
                    stub = service2_pb2_grpc.Service2Stub(channel)
                    status_request = service2_pb2.StatusRequest(phone=user.phone, status="OK")
                    stub.InsertStatus(status_request)
            self.db_conn.commit()
        return service1_pb2.Response(result="Users inserted and status updated successfully")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service1 = Service1()
    service1_pb2_grpc.add_Service1Servicer_to_server(service1, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
