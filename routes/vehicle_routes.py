from typing import List
from fastapi import APIRouter, HTTPException
from database import db_dependency
from schemas.vehicle_schema import (
    CreateVehicleSchema,
    UpdateVehicleSchema,
    VehicleSchema,
)
from models import Vehicle, VehicleImage
from utils.upload_file import upload_file
from utils.model import get_model_by_id, delete_model_by_id, get_all
from auth import protected


router = APIRouter(prefix="/vehicle", tags=["vehicle"])

router.dependencies.append(protected)


def get_vehicle(db: db_dependency, id: int):
    return get_model_by_id(Vehicle, id, db)


@router.get("", response_model=list[VehicleSchema])
async def get_all_vehicles(db: db_dependency):
    vehicles = db.query(Vehicle).all()

    return vehicles


@router.get("/{id}", response_model=VehicleSchema)
async def get_vehicle(db: db_dependency, id: int):
    vehicle = get_model_by_id(Vehicle, id, db)
    return vehicle


@router.post("/", response_model=VehicleSchema)
async def create(data: CreateVehicleSchema, db: db_dependency):
    vehicle = add_vehicle(data, db)

    return vehicle


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


@router.delete("/{id}")
async def delete_vehicle(id: int, db: db_dependency):
    delete_model_by_id(Vehicle, id, db)

    return {"message": "Vehicle deleted successfully"}


def add_vehicle(data: CreateVehicleSchema, db: db_dependency):
    validatedBody = data.model_dump()

    for index, image in enumerate(data.images):
        newImage = upload_file(image.url)
        validatedBody["images"][index] = VehicleImage(url=newImage.url)

    vehicle = Vehicle(**validatedBody)

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    db.commit()

    return vehicle
