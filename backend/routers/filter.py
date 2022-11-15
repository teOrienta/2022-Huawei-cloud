from utils import (filter_log, get_log_statistics, generate_svg,
                   list_to_eventlog, streaming_eventlog, database)
from pydantic import BaseModel, typing
from fastapi import APIRouter, status
from datetime import datetime

router = APIRouter(
    prefix="/api/filter",
    tags=['filter'],
    responses={404: {"Filter": "Not found"}}
)

class FilterInput(BaseModel):
    analysis: str
    detailLevel: int
    startDate: typing.Optional[str]
    endDate: str

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
    analysis = request.analysis
    end_date = request.endDate
    start_date = request.startDate
    dfg_detail_level = request.detailLevel

    if analysis == "live":
        event_log = streaming_eventlog.get()
    else:
        data = database.select_log_events(analysis = analysis)
        event_log = list_to_eventlog(data, {
            "case_id_key": "caseId",
            "resource_key": "resource",
            "activity_key": "activity",
            "timestamp_key": "endTimestamp",
            "start_timestamp_key": "startTimestamp"
        })

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    except: start_date = datetime(1970, 1, 1)
    
    try:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except: end_date = datetime.today()

    filtered_log = filter_log(event_log, start_date, end_date)

    if len(filtered_log) == 0:
        return status.HTTP_404_NOT_FOUND, {
            "message": "No events found in the given date range."
        }

    statistics = get_log_statistics(filtered_log)

    datail_percentage = dfg_detail_level * 20 / 100
    freq_svg_str, perf_svg_str = generate_svg(filtered_log, datail_percentage)

    return {
        "filters": request.dict(),
        "statistics": statistics,
        "freq_svg": freq_svg_str,
        "perf_svg": perf_svg_str
    }
