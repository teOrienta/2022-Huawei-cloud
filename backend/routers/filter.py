from datetime import datetime
from fastapi import APIRouter, status
from pydantic import BaseModel

from utils import filter_log, get_log_statistics, generate_svg
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

    filtered_log = filter_log(
        original_log,
        start_date=start_date,
        end_date=end_date
    )

    if len(filtered_log) == 0:
        print("log size 0.")
        return status.HTTP_404_NOT_FOUND

    get_cache().save_filtered_log(filtered_log)

    stats = get_log_statistics(filtered_log)

    dfg_detail_percentage = (1 + dfg_detail_level) * 20 / 100
    freq_dfg_file_path, perf_dfg_file_path = generate_svg(filtered_log, dfg_detail_percentage)

    with open(freq_dfg_file_path, encoding='utf-8') as file:
        freq_dfg_str = "".join(file.read().splitlines())

    with open(perf_dfg_file_path, encoding='utf-8') as file:
        perf_dfg_str = "".join(file.read().splitlines())
    
    return {
        "filters": {
            "exhibition": "frequency",
            "detail_level": dfg_detail_level,
            "startDate": start_date,
            "endDate": end_date
        },

        "statistics": stats,

        "freq_svg": freq_dfg_str,
        "perf_svg": perf_dfg_str
    }
