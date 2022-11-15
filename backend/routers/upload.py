from utils import (database, constants, as_form, csv_to_formatted_dict,
                   DEFAULT_START_TIMESTAMP_KEY, DEFAULT_NAME_KEY,
                   DEFAULT_RESOURCE_KEY, DEFAULT_TIMESTAMP_KEY)
from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel, typing

router = APIRouter(
    prefix="/api/upload",
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

class AnalysisOutputDTO(BaseModel):
    analysis: typing.List[str]

@router.post("/", response_model=UploadOutputDTO)
async def upload_csv(file: UploadFile,
                     request: UploadInputDTO = Depends(UploadInputDTO.as_form)):
    events_dict = csv_to_formatted_dict(file.file, {
        "case_id_key": request.case_id_key,
        "resource_key": request.resource_key,
        "activity_key": request.activity_key,
        "timestamp_key": request.timestamp_key,
        "start_timestamp_key": request.start_timestamp_key
    })
    database.insert_many_log_events([
        {
            "analysis": request.analysis_name,
            "caseId": event[constants.CASE_CONCEPT_NAME],
            "activity": event[DEFAULT_NAME_KEY],
            "resource": event.get(DEFAULT_RESOURCE_KEY),
            "endTimestamp": event[DEFAULT_TIMESTAMP_KEY],
            "startTimestamp": event.get(DEFAULT_START_TIMESTAMP_KEY,
                                        event[DEFAULT_TIMESTAMP_KEY])
        } for event in events_dict
    ])

    return { "analysis_name": request.analysis_name }

@router.get("/analysis", response_model=AnalysisOutputDTO)
async def get_analysis():
    return {
        "analysis": database.select_analysis()
    }