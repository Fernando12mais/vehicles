from fastapi import FastAPI
from models import User, Vehicle, Base, VehicleImage
from database import SessionLocal, engine

from routes.user_routes import router as user_routes
from routes.vehicle_routes import router as vehicle_routes
from routes.auth_routes import router as auth_routes

from fastapi.middleware.cors import CORSMiddleware
from auth import bcrypt_context
from utils.file import upload_image


app = FastAPI()


origins = ["*", "192.168.100.13:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


app.include_router(router=user_routes)
app.include_router(router=vehicle_routes)
app.include_router(auth_routes)


vehicles_to_add = [
    Vehicle(
        name="Toro 2020",
        brand="Fiat",
        model="Toro",
        images=[
            VehicleImage(
                **upload_image(
                    "https://images.prd.kavak.io/eyJidWNrZXQiOiJrYXZhay1pbWFnZXMiLCJrZXkiOiJpbWFnZXMvMjk3OTE0L0VYVEVSSU9SLWZyb250U2lkZVBpbG90TmVhci0xNzA2MDMzNzM1MDI3LmpwZWciLCJlZGl0cyI6eyJyZXNpemUiOnsid2lkdGgiOjU0MCwiaGVpZ2h0IjozMTB9fX0="
                )
            )
        ],
        price=130899,
    ),
    Vehicle(
        name="Cherry 2022",
        brand="Arizo",
        model="Cherry",
        images=[
            VehicleImage(
                **upload_image(
                    "https://images.prd.kavak.io/eyJidWNrZXQiOiJrYXZhay1pbWFnZXMiLCJrZXkiOiJpbWFnZXMvMjk2NzE0L0VYVEVSSU9SLWZyb250U2lkZVBpbG90TmVhci0xNzA1MzQyNTU3ODAyLmpwZWciLCJlZGl0cyI6eyJyZXNpemUiOnsid2lkdGgiOjU0MCwiaGVpZ2h0IjozMTB9fX0="
                )
            )
        ],
        price=111199,
    ),
    Vehicle(
        name="Citroen 2019",
        brand="Citroen",
        model="Aircross",
        images=[
            VehicleImage(
                **upload_image(
                    "https://images.prd.kavak.io/eyJidWNrZXQiOiJrYXZhay1pbWFnZXMiLCJrZXkiOiJpbWFnZXMvMjk2NTU2L0VYVEVSSU9SLWZyb250U2lkZVBpbG90TmVhci0xNzA1NTE5NTQ1MjQwLmpwZWciLCJlZGl0cyI6eyJyZXNpemUiOnsid2lkdGgiOjU0MCwiaGVpZ2h0IjozMTB9fX0="
                )
            )
        ],
        price=61799,
    ),
    Vehicle(
        name="Chevrolet 2019",
        brand="Chevrolet",
        model="Prisma",
        images=[],
        price=60799,
    ),
]


def add_default_data():
    session = SessionLocal()
    users = session.query(User).all()

    if not users:
        user = User(
            name="Admin",
            email="admin@email.com",
            password=bcrypt_context.hash("@admin"),
        )

        session.add(user)
        session.commit()

    vehicles = session.query(Vehicle).all()

    if not vehicles:
        for vehicle in vehicles_to_add:
            session.add(vehicle)

        session.commit()


add_default_data()
