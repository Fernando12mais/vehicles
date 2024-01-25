from sqlalchemy import Column, String, Integer
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    brand = Column(String)
    model = Column(String)
    picture = Column(String)
    price = Column(Integer)
