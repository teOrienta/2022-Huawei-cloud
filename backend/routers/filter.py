from utils import (filter_log, get_log_statistics, generate_svg,
                   streaming_eventlog, eventlog_cache)
from pydantic import BaseModel, typing
from fastapi import APIRouter, status
from datetime import datetime

router = APIRouter(
    prefix="/api/filter",
    tags=['filter'],
    responses={404: {"Filter": "Not found"}}
)

class FilterInput(BaseModel):
    startDate: typing.Optional[str]
    endDate: str
    detailLevel: int

class StatisticsDTO(BaseModel):
    cases: int
    activities: int
    averageCaseDuration: float
    averageActivityDuration: float

class FilterOutputDTO(BaseModel):
    filters: FilterInput
    freq_svg: typing.Any
    perf_svg: typing.Any
    statistics: StatisticsDTO


@router.post("/", response_model=FilterOutputDTO)
async def filter(request: FilterInput):
    end_date = request.endDate
    start_date = str(request.startDate)
    dfg_detail_level = request.detailLevel

    original_log = streaming_eventlog.get()
    eventlog_cache.save_log(original_log)

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    except: start_date = datetime(1970, 1, 1)
    
    try:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except: end_date = datetime.today()

    filtered_log = filter_log(
        original_log,
        start_date=start_date,
        end_date=end_date
    )

    if len(filtered_log) == 0:
        return status.HTTP_404_NOT_FOUND, {
            "message": "No events found in the given date range."
        }

    eventlog_cache.save_filtered_log(filtered_log)
    statistics = get_log_statistics(filtered_log)

    dfg_detail_percentage = dfg_detail_level * 20 / 100
    freq_svg_str, perf_svg_str = generate_svg(filtered_log, dfg_detail_percentage)

    return {
        "filters": request.dict(),
        "statistics": statistics,
        "freq_svg": freq_svg_str,
        "perf_svg": perf_svg_str
    }
