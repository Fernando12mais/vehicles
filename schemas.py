from pydantic import BaseModel


class VehicleCreate(BaseModel):
    id: int
    name: str
    brand: str
    model: str
    picture: str
