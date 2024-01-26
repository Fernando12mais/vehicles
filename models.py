from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String, index=True)
    password = Column(String)


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    brand = Column(String)
    model = Column(String)
    price = Column(Integer)

    images = relationship("VehicleImage", back_populates="vehicle")


class VehicleImage(Base):
    __tablename__ = "vehicle_images"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))

    vehicle = relationship("Vehicle", back_populates="images")


class Token(Base):
    __tablename__ = "token"
    token = Column(String, unique=True, primary_key=True)
    valid = Column(Boolean)
    expiration = Column(DateTime)
