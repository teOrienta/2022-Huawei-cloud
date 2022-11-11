from fastapi import APIRouter

from ..config import database

router = APIRouter(
    prefix="/lister",
    tags=['lister'],
    responses={404: {"Lister": "Not found"}}
)

@router.get("/municipio/")
async def get_municipios_list():
    municipios = database.get_all_municipios()

    return {
        "municipios": municipios
    }


@router.get("/modalidades/")
async def get_modalidades_list():
    modalidades = database.get_all_modalidades()

    return {
        "modalidades": modalidades
    }

