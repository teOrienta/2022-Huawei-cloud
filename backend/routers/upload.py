from utils import (eventlog_cache, as_form, csv_file_to_eventlog,
                   generate_svg, get_log_statistics)
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
        "case_id_key": str(request.case_id_key),
        "resource_key": str(request.resource_key),
        "activity_key": str(request.activity_key),
        "timestamp_key": request.timestamp_key,
        "start_timestamp_key": str(request.start_timestamp_key)
    })
    freq_svg_str, perf_svg_str = generate_svg(event_log)
    statistics = get_log_statistics(event_log)
    eventlog_cache.save_log(event_log)
    return {
        "analysis_name": str(request.analysis_name),
        "statistics": statistics,
        "freq_svg": FileResponse(freq_svg_str),
        "perf_svg": FileResponse(perf_svg_str)
    }
