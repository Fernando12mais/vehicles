from typing import Optional, List
from pydantic import BaseModel


class CreateVehicleImageSchema(BaseModel):
    url: str


class VehicleImageSchema(CreateVehicleImageSchema):
    id: int
    file_id: str


class VehicleSchema(BaseModel):
    id: int
    name: str
    brand: str
    model: str
    price: int
    images: List[VehicleImageSchema]

    class Config:
        from_attributes = True


class CreateVehicleSchema(BaseModel):
    name: str
    brand: str
    model: str
    price: int
    images: List[CreateVehicleImageSchema]


class UpdateVehicleSchema(VehicleSchema):
    id: int
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    picture: Optional[str] = None
    images: List[CreateVehicleImageSchema]
