from fastapi import APIRouter, HTTPException, Depends
from auth import authenticate_user, create_access_token, protected
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from database import db_dependency
from starlette import status
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(data.username, data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
        )
    token = create_access_token(user.name, user.id, timedelta(minutes=30))

    return {
        "message": "Usuário logado com sucesso!",
        "access_token": token,
        "token_type": "bearer",
    }


router.dependencies.append(protected)


@router.get("/is-authenticated")
async def is_authenticated():
    return {"authorized": True}
