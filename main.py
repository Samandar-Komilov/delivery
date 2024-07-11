from fastapi import FastAPI, Depends
from auth.routes import router as auth_router
from orders.routes import router as order_router
from products.routes import router as product_router

from models import User
import crud


app = FastAPI()
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(product_router)


@app.get("/")
async def root():
    return {'message': 'FastAPI is working!'}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(crud.get_current_user)):
    return current_user


if __name__ == '__main__':
    import uvicorn
    from database import init_db
    init_db()
    uvicorn.run('main:app', reload=True)