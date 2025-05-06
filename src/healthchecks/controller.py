from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.healthchecks.schemas import HealthCheckOut

router = APIRouter(tags=['healthchecks'])


@router.head(
    '/v0/ping',
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckOut,
)
@router.get(
    '/v0/ping',
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckOut,
)
async def ping() -> JSONResponse:
    return JSONResponse(
        content={'status': 'OK'}, status_code=status.HTTP_200_OK
    )
