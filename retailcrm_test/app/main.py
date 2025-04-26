from contextlib import asynccontextmanager

from app.api.api_v1.customers import router as customers_router
from app.api.api_v1.orders import router as orders_router
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


root_path = "/api/v1"
main_app = FastAPI(lifespan=lifespan, root_path=root_path)
main_app.include_router(customers_router, prefix="")
main_app.include_router(orders_router, prefix="")
