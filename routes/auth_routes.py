from fastapi import APIRouter, HTTPException, Depends, Request
from auth import authenticate_user, create_access_token, protected, auth_dependency
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from database import db_dependency
from starlette import status
from datetime import timedelta
from models import Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(data.username, data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
        )
    token = create_access_token(user.name, user.id, timedelta(minutes=20))

    db.add(token)
    db.commit()

    return {
        "message": "Usuário logado com sucesso!",
        "access_token": token.token,
        "token_type": "bearer",
    }


router.dependencies.append(protected)


@router.get("/is-authenticated")
async def is_authenticated():
    return {"authorized": True}


@router.post("/logout", status_code=status.HTTP_200_OK)
async def is_authenticated(db: db_dependency, request: Request):
    authorization = request.headers.get("Authorization").replace("Bearer ", "")
    token = db.query(Token).filter(Token.token == authorization).first()

    token.valid = False
    db.commit()

    return True
