from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    email: str | None = None
    is_active: bool | None = None

class UserInDB(User):
    password: str


class SignupModel(BaseModel):
    username: str
    email: str
    password: str


class LoginModel(BaseModel):
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class OrderModel(BaseModel):
    quantity: int
    order_status: Optional[str] = "PENDING"
    user_id: Optional[int]
    product_id: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "quantity": 2,
                "order_statuses": "PENDING",
                "user_id": 1,
                "product_id": 1,
            }
        }
    }


class OrderStatusModel(BaseModel):
    order_status: Optional[str] = "PENDING"

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "order_status": "PENDING"
            }
        }
    }


class ProductModel(BaseModel):
    name: str
    price: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "name": "Uzbek plov",
                "price": 30000
            }
        }
    }