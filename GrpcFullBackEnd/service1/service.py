import psycopg2
import redis
import time
from concurrent import futures
import grpc
import service1_pb2
import service1_pb2_grpc
from datetime import datetime


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
                time.sleep(5)
        raise Exception("Could not connect to the database after several attempts")

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(40),
            national_id VARCHAR(20),
            phone VARCHAR(12),
            message TEXT,
            status BOOLEAN,
            dc_sent_time TIMESTAMP
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
                cursor.execute(
                    "INSERT INTO users (name, national_id, phone, message, status, dc_sent_time) VALUES (%s, %s, %s, %s, %s, %s)",
                    (user.name, user.national_id, user.phone, request.message, True, datetime.now())
                )
            self.db_conn.commit()
        return service1_pb2.Response(result="Users inserted and status updated successfully")

    def GetUsersByNationalId(self, request, context):
        with self.db_conn.cursor() as cursor:
            cursor.execute("SELECT name, national_id, phone, message FROM users WHERE national_id = %s",
                           (request.national_id,))
            rows = cursor.fetchall()
            users = [service1_pb2.User(name=row[0], national_id=row[1], phone=row[2], message=row[3]) for row in rows]
        return service1_pb2.UserList(users=users)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service1 = Service1()
    service1_pb2_grpc.add_Service1Servicer_to_server(service1, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
