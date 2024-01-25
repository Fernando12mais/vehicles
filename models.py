from sqlalchemy import Column, String, Integer
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    password = Column(String)


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    brand = Column(String)
    model = Column(String)
    picture = Column(String)
    price = Column(Integer)
