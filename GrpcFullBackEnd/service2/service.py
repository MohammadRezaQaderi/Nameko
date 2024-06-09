import psycopg2
import redis
from concurrent import futures
import grpc
import service2_pb2
import service2_pb2_grpc


class Service2(service2_pb2_grpc.Service2Servicer):

    def __init__(self):
        self.db_conn = self.connect_to_database()
        self.redis_conn = redis.StrictRedis(host='service2_redis', port=6379, db=0)
        self.create_table()

    def connect_to_database(self):
        try:
            return psycopg2.connect("dbname=service2_db user=service2_user password=service2_pass host=service2_db")
        except psycopg2.OperationalError:
            conn = psycopg2.connect("dbname=service2_db user=service2_user password=service2_pass host=service2_db")
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute("CREATE DATABASE service1_db")
            return psycopg2.connect("dbname=service2_db user=service2_user password=service2_pass host=service2_db")

    def create_table(self):
        create_table_query = """
    CREATE TABLE IF NOT EXISTS status_table (
        phone VARCHAR(15) PRIMARY KEY,
        status VARCHAR(100)
    );
    """
        with self.db_conn.cursor() as cursor:
            cursor.execute(create_table_query)
            self.db_conn.commit()

    def AnotherFunction(self, request, context):
        with grpc.insecure_channel('service1:50051') as channel:
            stub = service1_pb2_grpc.Service1Stub(channel)
            service1_response = stub.SomeFunction(service1_pb2.Request(parameter=request.parameter))

        response = service2_pb2.Response()
        response.result = "Processed " + request.parameter + " and got response: " + service1_response.result
        return response

    def InsertStatus(self, request, context):
        with self.db_conn.cursor() as cursor:
            cursor.execute("INSERT INTO status_table (phone, status) VALUES (%s, %s)", (request.phone, request.status))
            self.db_conn.commit()
        return service2_pb2.Response(result="Status inserted successfully")

    def GetStatus(self, request, context):
        phone = request.phone
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT phone, status FROM status_table WHERE phone = %s", (phone,))
        result = cursor.fetchone()
        cursor.close()

        if result is None:
            return service2_pb2.StatusResponse(status="")

        return service2_pb2.StatusResponse(status=result[0])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service2 = Service2()
    service2_pb2_grpc.add_Service2Servicer_to_server(service2, server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
