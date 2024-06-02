import uuid
from nameko.rpc import rpc
import psycopg2
import redis


class AirportsService:
    name = "airports_service"

    def __init__(self):
        self.db_conn = psycopg2.connect("dbname=service1_db user=service1_user password=service1_pass host=service1_db")
        self.redis_conn = redis.StrictRedis(host='service1_redis', port=6379, db=0)

    @rpc
    def get(self, airport_id):
        airport = self.redis_conn.get(airport_id)
        return airport

    @rpc
    def create(self, airport):
        airport_id = uuid.uuid4().hex
        self.redis_conn.set(airport_id, airport)
        return airport_id
