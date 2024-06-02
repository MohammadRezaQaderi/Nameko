import uuid
from nameko.rpc import rpc
import psycopg2
import redis


class TripsService:
    name = "trips_service"

    def __init__(self):
        self.db_conn = psycopg2.connect("dbname=service1_db user=service1_user password=service1_pass host=service1_db")
        self.redis_conn = redis.StrictRedis(host='service2_redis', port=6379, db=0)

    @rpc
    def get(self, trip_id):
        trip = self.redis_conn.get(trip_id)
        return trip

    @rpc
    def create(self, airport_from_id, airport_to_id):
        trip_id = uuid.uuid4().hex
        self.redis_conn.set(trip_id, {
            "from": airport_from_id,
            "to": airport_to_id
        })
        return trip_id
