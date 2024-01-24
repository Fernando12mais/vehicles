from fastapi import APIRouter
from database import db_dependency
from schemas import VehicleCreate
from models import Vehicle


router = APIRouter()


@router.post(
    "/create",
)
async def create(data: VehicleCreate, db: db_dependency):
    vehicle = Vehicle(**data.model_dump())

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return vehicle


# async def create(vehicle: Vehicle, db: db_dependency):
#     print(db)
#     # newVehicle = Vehicle(vehicle)
#     # db.add(newVehicle)
#     # db.commit()
#     # db.refresh(vehicle)

#     return {"message": "Veículo adicionado com sucesso!"}
