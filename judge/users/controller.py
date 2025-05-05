from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import UUID4
from judge.contrib.documentation import (
    NotFoundErrorResponse,
    UnprocessableEntityErrorResponse,
    InternalServerErrorResponse,
)
from judge.users.schemas import (
    UserCollectionResponse,
    UserIn,
    UserOut,
)
from judge.users.usecases import UserUseCase
from judge.contrib.exceptions import ObjectNotFound

router = APIRouter(tags=["users"], prefix="/v0/users")

@router.post(
    '',
    summary='Create a new user',
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
    responses={
        201: {'model': UserOut},
        404: {'model': NotFoundErrorResponse},
        422: {'model': UnprocessableEntityErrorResponse},
        500: {'model': InternalServerErrorResponse},
    },
)
async def post(
    use_case: UserUseCase = Depends(),
    user_in: UserIn = Body(...),
) -> UserOut:
    user = await use_case.create(user_in=user_in)

    return user


@router.get(
    '/{id}',
    summary='Get a User by id',
    status_code=status.HTTP_200_OK,
    response_model=UserOut,
    responses={
        200: {'model': UserOut},
        404: {'model': NotFoundErrorResponse},
        500: {'model': InternalServerErrorResponse},
    },
)
async def get(
    id: UUID4,
    use_case: UserUseCase = Depends(),
) -> UserOut:
    try:
        user = await use_case.get(id=id)
    except ObjectNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


@router.get(
    '',
    summary='List users',
    status_code=status.HTTP_200_OK,
    response_model=UserCollectionResponse,
    responses={
        200: {'model': UserCollectionResponse},
        500: {'model': InternalServerErrorResponse},
    },
)
async def query(
    use_case: UserUseCase = Depends(),
) -> UserCollectionResponse:
    users = await use_case.query()

    return users
