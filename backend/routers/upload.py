from utils import (eventlog_cache, database, as_form, generate_svg,
                   csv_file_to_eventlog, get_log_statistics, constants,
                   DEFAULT_START_TIMESTAMP_KEY, DEFAULT_NAME_KEY,
                   DEFAULT_RESOURCE_KEY, DEFAULT_TIMESTAMP_KEY)
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, typing

router = APIRouter(
    prefix="/upload",
    tags=['upload'],
    responses={404: {"Upload": "Not found"}}
)

@as_form
class UploadInputDTO(BaseModel):
    analysis_name: str
    file: UploadFile
    case_id_key: str
    activity_key: str
    timestamp_key: str
    resource_key: str = ""
    start_timestamp_key: str = ""

class StatisticsDTO(BaseModel):
    cases: int
    activities: int
    averageCaseDuration: float
    averageActivityDuration: float

class UploadOutputDTO(BaseModel):
    analysis_name: str
    freq_svg: typing.Any
    perf_svg: typing.Any
    statistics: StatisticsDTO

@router.post("/upload", response_model=UploadOutputDTO)
async def upload_csv(file: UploadFile,
                     request: UploadInputDTO = Depends(UploadInputDTO.as_form)):
    event_log = csv_file_to_eventlog(file.file, {
        "case_id_key": request.case_id_key,
        "resource_key": request.resource_key,
        "activity_key": request.activity_key,
        "timestamp_key": request.timestamp_key,
        "start_timestamp_key": request.start_timestamp_key
    })
    freq_svg_str, perf_svg_str = generate_svg(event_log)
    statistics = get_log_statistics(event_log)
    eventlog_cache.save_log(event_log)
    database.insert_many_log_events([
        {
            "analysis": request.analysis_name,
            "caseId": trace.attributes[DEFAULT_NAME_KEY],
            "activity": event[DEFAULT_NAME_KEY],
            "resource": event.get(DEFAULT_RESOURCE_KEY),
            "endTimestamp": event[DEFAULT_TIMESTAMP_KEY],
            "startTimestamp": event.get(DEFAULT_START_TIMESTAMP_KEY,
                                        event[DEFAULT_TIMESTAMP_KEY])
        } for trace in event_log for event in trace
    ])

    return {
        "analysis_name": request.analysis_name,
        "freq_svg": FileResponse(freq_svg_str),
        "perf_svg": FileResponse(perf_svg_str),
        "statistics": statistics
    }
