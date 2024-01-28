from fastapi import APIRouter, HTTPException
from database import db_dependency
from utils.file import upload_image
from schemas.vehicle_schema import (
    CreateVehicleSchema,
    UpdateVehicleSchema,
    VehicleSchema,
)
from models import Vehicle, VehicleImage
from utils.file import upload_file, delete_file
from utils.model import get_model_by_id, delete_model_by_id
from auth import protected
from sqlalchemy import or_
from starlette import status


router = APIRouter(prefix="/vehicle", tags=["vehicle"])


def get_vehicle(db: db_dependency, id: int):
    return get_model_by_id(Vehicle, id, db)


def add_vehicle(data: CreateVehicleSchema, db: db_dependency):
    validatedBody = data.model_dump()

    for index, image in enumerate(data.images):
        newImage = upload_file(image.url)
        validatedBody["images"][index] = VehicleImage(
            url=newImage.url, file_id=newImage.file_id if newImage.file_id else None
        )

    vehicle = Vehicle(**validatedBody)

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return vehicle


@router.get("", response_model=list[VehicleSchema])
async def get_all_vehicles(db: db_dependency, search: str = ""):
    search_fields = [Vehicle.brand, Vehicle.name, Vehicle.model]
    conditions = or_(*[field.ilike(f"%{search}%") for field in search_fields])
    vehicles = db.query(Vehicle).filter(conditions).order_by(Vehicle.price).all()

    return vehicles


@router.get("/{id}", response_model=VehicleSchema)
async def get_vehicle(db: db_dependency, id: int) -> VehicleSchema:
    vehicle = get_model_by_id(Vehicle, id, db)
    return vehicle


router.dependencies.append(protected)


@router.post("", response_model=VehicleSchema, status_code=status.HTTP_201_CREATED)
async def create(data: CreateVehicleSchema, db: db_dependency):
    vehicle = add_vehicle(data, db)

    return vehicle


@router.put("", status_code=status.HTTP_200_OK)
async def update_vehicle(data: UpdateVehicleSchema, db: db_dependency):
    vehicle = await get_vehicle(db, data.id)

    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    updated_data = data.model_dump(exclude=["id", "images"])
    for image in data.images:
        db_image = (
            db.query(VehicleImage)
            .filter(
                VehicleImage.url == image.url and VehicleImage.vehicle_id == vehicle.id
            )
            .first()
        )
        if not db_image:
            new_image = VehicleImage(**upload_image(image.url), vehicle_id=vehicle.id)
            db.add(new_image)
            db.commit()

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


@router.delete("/images/{file_ids}")
def delete_image(file_ids: str, db: db_dependency):
    ids = file_ids.split(",")

    for id in ids:
        delete_file(file_id=id)
        db.query(VehicleImage).filter(VehicleImage.file_id == id).delete()
        db.commit()

    return
