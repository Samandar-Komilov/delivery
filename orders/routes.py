from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from crud import get_current_user, get_admin_user
from models import User, Order
from database import get_db
from schemas import OrderModel, OrderStatusModel

router = APIRouter(prefix="/orders", tags=["Orders"])

# session = session(bind=engine)

@router.get("/")
async def welcome_page(
    current_user: User = Depends(get_current_user),
):
    return {"message": "Bu Order route sahifasi"}


@router.post("/make", status_code=status.HTTP_201_CREATED)
async def make_order(
    order: OrderModel, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
    ):
    new_order = Order(
        quantity=order.quantity,
        product_id=order.product_id
    )
    new_order.user = current_user
    session.add(new_order)
    session.commit()

    data = {
        "success": True,
        "code": 201,
        "message": "Order is created successfully.",
        "data": {
            "id": new_order.id,
            "name": new_order.product.name,
            "price": new_order.product.price
        },
        "quantity": new_order.quantity,
        "order_status": new_order.order_statuses.value,
        "total_price": new_order.quantity * new_order.product.price
    }

    return jsonable_encoder(data)


@router.get("/list", status_code=status.HTTP_200_OK)
async def list_all_orders(
    current_user: User = Depends(get_admin_user),
    session: Session = Depends(get_db)
    ):
    orders = session.query(Order).all()
    custom_data = [
        {
            "id": order.id,
            "user": {
                "id": order.user.id,
                "username": order.user.username,
                "email": order.user.email
            },
            "product": {
                "id": order.product.id,
                "name": order.product.name,
                "price": order.product.price
            },
            "quantity": order.quantity,
            "order_statuses": order.order_statuses.value,
            "total_price": order.quantity * order.product.price
        } for order in orders
    ]

    return jsonable_encoder(custom_data)


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_order_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
    ):
    order = session.query(Order).filter(Order.id == id).first()

    if order:
        custom_order = {
            "id": order.id,
            "user": {
                "id": order.user.id,
                "username": order.user.username,
                "email": order.user.email
            },
                "product": {
                "id": order.product.id,
                "name": order.product.name,
                "price": order.product.price
            },
            "quantity": order.quantity,
            "order_statuses": order.order_statuses.value,
            "total_price": order.quantity * order.product.price
        }
        return jsonable_encoder(custom_order)
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order with {id} ID is not found")
    

@router.get("users/{username}/orders", status_code=status.HTTP_200_OK)
async def get_user_orders(
    username: User.username = Depends(get_current_user),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
    ):

    custom_data = [
        {
            "id": order.id,
            "user": {
                "id": order.user.id,
                "username": order.user.username,
                "email": order.user.email
            },
            "product": {
                "id": order.product.id,
                "name": order.product.name,
                "price": order.product.price
            },
            "quantity": order.quantity,
            "order_statuses": order.order_statuses.value,
            "total_price": order.quantity * order.product.price
        } for order in current_user.orders
    ]
    return jsonable_encoder(custom_data)


@router.get("users/{username}/order/{id}")
async def get_user_order_by_id(
    id: int,
    username: User.username = Depends(get_current_user),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
    ):
    order = session.query(Order).filter(Order.id == id, Order.user == current_user).first()

    if order:
        order_data = {
            "id": order.id,
            "user": {
                "id": order.user.id,
                "username": order.user.username,
                "email": order.user.email
            },
            "product": {
                "id": order.product.id,
                "name": order.product.name,
                "price": order.product.price
            },
            "quantity": order.quantity,
            "order_statuses": order.order_statuses.value,
            "total_price": order.quantity * order.product.price
        }
        return jsonable_encoder(order_data)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No order exist with this ID: {id}")
    

@router.put("/{id}/update", status_code=status.HTTP_200_OK)
async def update_order(
    id: int,
    order: OrderModel,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
    ):
    order_to_update = session.query(Order).filter(Order.id == id).first()
    if order_to_update.user != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Kechirasiz, siz boshqa foydalanuvchilarning buyurtmalarini tahrirlay olmaysiz!")
    
    order_to_update.quantity = order.quantity
    order_to_update.product_id = order.product_id
    session.commit()

    custom_response = {
        "success": True,
        "code": 200,
        "message": "Sizning buyurtmangiz muvaffaqiyatli o'zgartirildi",
        "data": {
            "id": order.id,
            "quantity": order.quantity,
            "product": order.product_id,
            "order_status": order.order_statuses
        }
    }
    return jsonable_encoder(custom_response)


@router.patch("/id/update-status", status_code=status.HTTP_200_OK)
async def update_order_status(
    id: int,
    order: OrderStatusModel,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
    ):
    order_to_update = session.query(Order).filter(Order.id == id).first()
    order_to_update.order_statuses = order.order_status
    session.commit()

    custom_response = {
        "success": True,
        "code": 200,
        "message": "User order is succesfully updated",
        "data": {
            "id": order_to_update.id,
            "order_status": order_to_update.order_statuses
        }
    }
    return jsonable_encoder(custom_response)


@router.delete("/id/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
    ):
    order = session.query(Order).filter(Order.id == id).first()
    if order.user != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Kechirasiz, siz boshqa foydalanuvchilarning buyurtmalarini o'chira olmaysiz!")

    if order.order_statuses != "PENDING":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Kechirasiz, siz yolga chiqqan va yetkazib berilgan buyurtmalarni o'chira olmaysiz!")

    session.delete(order)
    session.commit()

    custom_response = {
        "success": True,
        "code": 200,
        "message": "User order is successfully deleted.",
        "data": None
    }
    return jsonable_encoder(custom_response)