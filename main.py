from fastapi import FastAPI
import models
from database import engine, db_dependency

from routes.user_routes import router as user_routes
from routes.vehicle_routes import router as vehicle_routes

from dotenv import load_dotenv

load_dotenv()


from upload_file import upload_file


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


app.include_router(router=user_routes, prefix="/user", tags=["user"])
# app.include_router(router=vehicle_routes, prefix="/vehicle", tags=["vehicle"])


@app.get("/")
async def index(db: db_dependency):
    user = models.User(name="Fernando")

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Hello world", "user": user}


@app.get("/upload/{file}")
async def handle_upload(file: str):
    test = await upload_file(file)
    test
    return test


# @app.get("/test/{id}")
# async def get_test_id(id: int):
#     return {"id": id}
