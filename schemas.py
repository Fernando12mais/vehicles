from typing import Optional
from pydantic import BaseModel


class VehicleSchema(BaseModel):
    id: int
    name: str
    brand: str
    model: str
    picture: str
    price: int


class CreateVehicleSchema(VehicleSchema):
    id: None = None


class UpdateVehicleSchema(VehicleSchema):
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    picture: Optional[str] = None
    price: Optional[int] = None
