from pickle import NONE
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
    file_id = Column(String)

    vehicle = relationship("Vehicle", back_populates="images")
