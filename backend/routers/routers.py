from fastapi import APIRouter
from routers import filter

routers = APIRouter()

routers.include_router(filter.router)
