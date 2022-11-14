from utils import (filter_log, get_log_statistics, generate_svg,
                   streaming_eventlog, eventlog_cache)
from fastapi.responses import FileResponse
from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix="/api/filter",
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

    original_log = streaming_eventlog.get()
    eventlog_cache.save_log(original_log)

    if not start_date:        
        start_date = datetime(1970, 1, 1)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    if not end_date:
        end_date = datetime.today()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    filtered_log = filter_log(
        original_log,
        start_date=start_date,
        end_date=end_date
    )

    if len(filtered_log) == 0:
        return status.HTTP_404_NOT_FOUND

    eventlog_cache.save_filtered_log(filtered_log)
    statistics = get_log_statistics(filtered_log)

    dfg_detail_percentage = (1 + dfg_detail_level) * 20 / 100
    freq_svg_str, perf_svg_str = generate_svg(filtered_log, dfg_detail_percentage)

    return {
        "filters": request.dict(),
        "statistics": statistics,
        "freq_svg": FileResponse(freq_svg_str),
        "perf_svg": FileResponse(perf_svg_str)
    }
