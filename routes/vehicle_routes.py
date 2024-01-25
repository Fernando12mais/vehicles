from typing import List
from fastapi import APIRouter, HTTPException
from database import db_dependency
from schemas import CreateVehicleSchema, UpdateVehicleSchema
from models import Vehicle
from utils.upload_file import upload_file


router = APIRouter()


def get_vehicle(db: db_dependency, vehicle_id: int):
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()


@router.get("/")
async def get_all_vehicles(db: db_dependency):
    return db.query(Vehicle).all()


@router.post("/")
async def create(data: CreateVehicleSchema, db: db_dependency):
    result = upload_file(data.picture)

    validatedBody = data.model_dump()
    validatedBody["picture"] = result.url
    vehicle = Vehicle(**validatedBody)

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return {"message": "Veículo adicionado com sucesso!", "vehicle": vehicle}


@router.put("/")
async def update_vehicle(data: UpdateVehicleSchema, db: db_dependency):
    vehicle = get_vehicle(db, data.id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    result = upload_file(data.picture).url if data.picture else vehicle.picture

    updated_data = data.model_dump()
    updated_data["picture"] = result

    for key, value in updated_data.items():
        if value:
            setattr(vehicle, key, value)

    db.commit()
    db.refresh(vehicle)
    return vehicle


@router.delete("/{vehicle_id}")
async def delete_vehicle(vehicle_id: int, db: db_dependency):
    vehicle = get_vehicle(db, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    db.delete(vehicle)
    db.commit()

    return {"message": "Vehicle deleted successfully"}
