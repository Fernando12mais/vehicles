from fastapi import APIRouter, HTTPException
from database import db_dependency
from schemas.vehicle_schema import UpdateVehicleSchema
from models import User
from schemas.user_schema import CreateUserSchema
from utils.model import get_model_by_id, delete_model_by_id, get_all
from auth import bcrypt_context, auth_dependency
from starlette import status


router = APIRouter(prefix="/user", tags=["user"])


def get_user(db: db_dependency, id: int):
    return get_model_by_id(User, id, db)


@router.get("/")
async def get_user(user: auth_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"User": user.items()}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(data: CreateUserSchema, db: db_dependency):
    newUser = User(name=data.name, password=bcrypt_context.hash(data.password))

    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return {"message": "Usuário criado com sucesso!", "user": newUser}


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


@router.delete("/{id}")
async def delete_user(id: int, db: db_dependency):
    delete_model_by_id(User, id, db)

    return {"message": "User deleted successfully"}
