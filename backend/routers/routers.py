from fastapi import APIRouter
from routers import filter
from routers import lister

routers = APIRouter()

routers.include_router(filter.router)
routers.include_router(lister.router)
