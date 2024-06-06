from .models import UserPhone, Base
from nameko.rpc import rpc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis
import os


class Microservice2:
    name = "microservice2"

    db_uri = os.getenv('DB_URI')
    redis_uri = os.getenv('REDIS_URI')

    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    r = redis.Redis.from_url(redis_uri)

    @rpc
    def add_user_phone(self, user_id, phone, status):
        session = self.Session()
        user_phone = UserPhone(user_id=user_id, phone=phone, status=status)
        session.add(user_phone)
        session.commit()
        session.close()

        self.r.set(f"user_phone:{user_id}", phone)

        return f"User phone {phone} with status {status} added for user {user_id}"

    @rpc
    def get_user_phone(self, user_id):
        phone = self.r.get(f"user_phone:{user_id}")
        if phone:
            return f"User phone from cache: {phone.decode()}"

        session = self.Session()
        user_phone = session.query(UserPhone).filter_by(user_id=user_id).first()
        session.close()

        if user_phone:
            self.r.set(f"user_phone:{user_id}", user_phone.phone)
            return f"User phone from DB: {user_phone.phone}"

        return "User phone not found"
