from routers import filter, upload
from fastapi import APIRouter

routers = APIRouter()

routers.include_router(filter.router)
routers.include_router(upload.router)
