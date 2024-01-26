from fastapi import APIRouter, HTTPException
from database import db_dependency
from schemas.vehicle_schema import UpdateVehicleSchema
from models import User
from schemas.user_schema import CreateUserSchema
from utils.model import get_model_by_id
from auth import bcrypt_context, protected
from starlette import status


router = APIRouter(prefix="/user", tags=["user"])


def get_user(db: db_dependency, id: int):
    return get_model_by_id(User, id, db)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(data: CreateUserSchema, db: db_dependency):
    newUser = User(
        name=data.name, email=data.email, password=bcrypt_context.hash(data.password)
    )
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return {"message": "Usuário criado com sucesso!", "user": newUser}


router.dependencies.append(protected)


@router.put("/")
async def update_user(data: UpdateVehicleSchema, db: db_dependency):
    user = get_user(db, data.id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in data.model_dump().items():
        if value:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
