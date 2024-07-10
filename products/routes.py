from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from schemas import ProductModel
from models import User, Product
from database import get_db
from crud import get_current_user, get_admin_user


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductModel,
    admin_user: User = Depends(get_admin_user),
    session: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        price=product.price
    )
    session.add(new_product)
    session.commit()

    data = {
        "success": True,
        "code": 201,
        "message": "Product is created successfully",
        "data": {
            "id": new_product.id,
            "name": new_product.name,
            "price": new_product.price
        }
    }
    return jsonable_encoder(data)


@router.get("/list", status_code=status.HTTP_200_OK)
async def list_all_products(
    current_user: User = Depends(get_admin_user),
    session: Session = Depends(get_db)):
    products = session.query(Product).all()
    custom_data = [
        {
           "id": product.id,
           "name": product.name,
           "price": product.price
        } for product in products
    ]

    return jsonable_encoder(custom_data)


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_product_by_id(
    id: int,
    current_user: User = Depends(get_admin_user),
    session: Session = Depends(get_db) 
    ):
    product = session.query(Product).filter(Product.id == id).first()
    if product:
        custom_order = {
            "id": product.id,
            "name": product.name,
            "price": product.price
        }
        return jsonable_encoder(custom_order)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with {id} ID is not found")
    

@router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_by_id(
    id: int,
    current_user: User = Depends(get_admin_user),
    session: Session = Depends(get_db)
    ):
    product = session.query(Product).filter(Product.id == id).first()
    if product:
        session.delete(product)
        session.commit()
        data = {
            "success": True,
            "code": 200,
            "message": f"Product with ID {id} has been deleted",
            "data": None
        }
        return jsonable_encoder(data)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with {id} ID is not found")
    

@router.put('/{id}/update')
async def update_product_by_id(
    id: int,
    update_data: ProductModel,
    admin_user: User = Depends(get_admin_user),
    session: Session = Depends(get_db)
    ):
    product = session.query(Product).filter(Product.id == id).first()
    if product:
        # update product
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(product, key, value)
        session.commit()
        data = {
            "success": True,
            "code": 200,
            "message": f"Product with ID {id} has been updated",
            "data": {
                "id": product.id,
                "name": product.name,
                "price": product.price
            }
        }
        return jsonable_encoder(data)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with ID {id} is not found")