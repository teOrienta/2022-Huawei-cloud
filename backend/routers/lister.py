from fastapi import APIRouter

from utils import database

router = APIRouter(
    prefix="/lister",
    tags=['lister'],
    responses={404: {"Lister": "Not found"}}
)

@router.get("/logs/")
async def get_log_list():
    logs = database.get_event_logs()

    return {
        "logs": logs
    }

