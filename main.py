from fastapi import FastAPI
from auth.routes import router as auth_router
from orders.routes import router as order_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(order_router)


@app.get("/")
async def root():
    return {'message': 'FastAPI is working!'}


if __name__ == '__main__':
    import uvicorn
    # from database import init_db
    # init_db()
    uvicorn.run('main:app', reload=True)