from fastapi import APIRouter

router = APIRouter(prefix="/orders")


@router.get("/")
async def orders_list():
    return {"message": "Orders uchun"}