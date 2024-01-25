from fastapi import FastAPI
import models
from database import engine

from routes.user_routes import router as user_routes
from routes.vehicle_routes import router as vehicle_routes


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


app.include_router(router=user_routes, prefix="/user", tags=["user"])
app.include_router(router=vehicle_routes, prefix="/vehicle", tags=["vehicle"])
