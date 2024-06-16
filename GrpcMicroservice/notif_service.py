from nameko_grpc.entrypoint import Grpc
from notif_pb2 import MessageToUsersReply, User, UserList
from notif_pb2_grpc import notifStub
import psycopg2
import redis
from datetime import datetime

grpc = Grpc.implementing(notifStub)


class NotifService:
    name = "notif_service"

    def __init__(self):
        self.db_conn = self.connect_to_database()
        self.redis_conn = redis.StrictRedis(host='notif_redis', port=6379, db=0)

        # Create table if it does not exist
        self.create_table()

    def connect_to_database(self):
        try:
            return psycopg2.connect("dbname=notif_db user=notif_user password=notif_pass host=notif_db")
        except psycopg2.OperationalError:
            # Database does not exist, create it
            conn = psycopg2.connect("dbname=postgres user=notif_user password=notif_pass host=notif_db")
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute("CREATE DATABASE notif_db")
            return psycopg2.connect("dbname=notif_db user=notif_user password=notif_pass host=notif_db")

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

    @grpc
    def GetUsersByNationalId(self, request, context):
        with self.db_conn.cursor() as cursor:
            cursor.execute("SELECT name, national_id, phone, message FROM users WHERE national_id = %s",
                           (request.national_id,))
            rows = cursor.fetchall()
            users = [User(name=row[0], national_id=row[1], phone=row[2], message=row[3]) for row in rows]
        return UserList(users=users)

    @grpc
    def SendMessageToUsers(self, request, context):
        with self.db_conn.cursor() as cursor:
            for user in request.users:
                cursor.execute(
                    "INSERT INTO users (name, national_id, phone, message, status, dc_sent_time) VALUES (%s, %s, %s, %s, %s, %s)",
                    (user.name, user.national_id, user.phone, request.message, True, datetime.now())
                )
            self.db_conn.commit()
        return MessageToUsersReply(response="Users inserted and status updated successfully")
