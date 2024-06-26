from nameko.rpc import rpc
import psycopg2
import redis
from datetime import datetime


class Service1:
    name = "service1"

    def __init__(self):
        self.db_conn = self.connect_to_database()
        self.redis_conn = redis.StrictRedis(host='service1_redis', port=6379, db=0)

        # Create table if it does not exist
        self.create_table()

    def connect_to_database(self):
        try:
            return psycopg2.connect("dbname=service1_db user=service1_user password=service1_pass host=service1_db")
        except psycopg2.OperationalError:
            # Database does not exist, create it
            conn = psycopg2.connect("dbname=postgres user=service1_user password=service1_pass host=service1_db")
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute("CREATE DATABASE service1_db")
            return psycopg2.connect("dbname=service1_db user=service1_user password=service1_pass host=service1_db")

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS phone_records (
            id SERIAL PRIMARY KEY,
            phone VARCHAR(15) NOT NULL,
            status VARCHAR(10) CHECK (status IN ('success', 'fail')),
            create_date_time TIMESTAMP NOT NULL,
            edit_date_time TIMESTAMP NOT NULL
        );
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(create_table_query)
            self.db_conn.commit()

    @rpc
    def hello(self, phone):
        with self.db_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM phone_records WHERE phone = %s", (phone,))
            record = cursor.fetchone()
            if record:
                return {
                    'id': record[0],
                    'phone': record[1],
                    'status': record[2],
                    'create_date_time': record[3].strftime("%Y-%m-%dT%H:%M:%S.%f"),
                    'edit_date_time': record[4].strftime("%Y-%m-%dT%H:%M:%S.%f")
                }
            else:
                return {"error": "Record not found"}

    @rpc
    def create(self, data):
        phone = data['phone']
        status = data['status']
        create_date_time = datetime.strptime(data['create_date_time'], "%Y-%m-%dT%H:%M:%S.%f")
        edit_date_time = datetime.strptime(data['edit_date_time'], "%Y-%m-%dT%H:%M:%S.%f")

        with self.db_conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO phone_records (phone, status, create_date_time, edit_date_time) VALUES (%s, %s, %s, %s) RETURNING id",
                (phone, status, create_date_time, edit_date_time)
            )
            record_id = cursor.fetchone()[0]
            self.db_conn.commit()
            return {"id": record_id, "status": "created"}
