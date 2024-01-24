from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
async def get():
    return {"teste": "aaa"}
