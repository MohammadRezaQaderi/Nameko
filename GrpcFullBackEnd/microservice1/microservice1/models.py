from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()


class UserPhone(Base):
    __tablename__ = 'user_phone'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    status = Column(String, nullable=False)


DB_URI = os.getenv('DB_URI')
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
