from datetime import datetime
from fastapi import APIRouter, status
from pydantic import BaseModel

from ..utils import filter_log
from ..config import get_cache

router = APIRouter(
    prefix="/filter",
    tags=['filter'],
    responses={404: {"Filter": "Not found"}}
)

class FilterInput(BaseModel):
    startDate: str
    endDate: str
    detailLevel: int

@router.post("/")
async def filter(request: FilterInput):
    start_date = request.startDate
    end_date = request.endDate
    dfg_detail_level = request.detailLevel

    original_log = get_cache().get_log()

    if (start_date == ""):        
        start_date = datetime(1970, 1, 1)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    if (end_date == ""):
        end_date = datetime.today()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    filtered_log, stats = filter_log(
        original_log,
        start_date=start_date,
        end_date=end_date,
        dfg_detail_level=dfg_detail_level
    )

    if len(filtered_log) == 0:
        print("log size 0.")
        return status.HTTP_404_NOT_FOUND

    get_cache().save_filtered_log(filtered_log)
    
    return stats
