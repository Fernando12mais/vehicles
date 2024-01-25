from fastapi import FastAPI
import models
from database import engine

from routes.user_routes import router as user_routes
from routes.vehicle_routes import router as vehicle_routes
from routes.auth_routes import router as auth_routes


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


app.include_router(router=user_routes)
app.include_router(router=vehicle_routes)
app.include_router(auth_routes)
