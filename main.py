from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import os

from routes.user_routes import router as user_routes

from dotenv import load_dotenv

load_dotenv()


from upload_file import upload_file


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


app.include_router(router=user_routes, prefix="/user", tags=["user"])


@app.get("/")
async def index(db: db_dependency):
    user = models.User(name="Fernando")

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Hello world", "user": user}


@app.get("/upload/{file}")
async def handle_upload(file: str):
    response = await upload_file(file)
    response
    return response


# @app.get("/test/{id}")
# async def get_test_id(id: int):
#     return {"id": id}
