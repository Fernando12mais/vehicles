from datetime import timedelta, datetime
from math import exp
from typing import Annotated
from fastapi import Depends, HTTPException
from database import db_dependency
from models import Token, User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

SECRET_KEY = "asdnasdouihasoiduhiusdhfisdgfuygasduyfgsduayfgusaydfguygsdfa"

ALGORITHM = "HS256"


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
    try:
        db_token = db.query(Token).filter(Token.token == token).first()
        if not token or db_token and not db_token.valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
            )

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
            )
        return {"username": username, "id": user_id}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
        )


protected = Depends(get_current_user)
auth_dependency = Annotated[dict, protected]


def authenticate_user(email: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_access_token(name: str, id: str, expiration: timedelta):
    encode = {"sub": name, "id": id}
    expires = datetime.utcnow() + expiration
    encode["exp"] = expires

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return Token(token=token, expiration=expires, valid=True)
