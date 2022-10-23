from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from apps.problems.crud import create, delete, get, get_all, update
from apps.problems.models import Problem
from apps.problems.schemas import ProblemIn, ProblemOut
from contrib import responses
from contrib.exceptions import ConflictObject, DuplicateObject, InvalidContent
from contrib.helpers import base64_decode
from converters.schemas import convert_model_to_schema
from database.session import Base, engine, get_database

Base.metadata.create_all(bind=engine)

problem_router = APIRouter()


@problem_router.get(
    '/problems',
    summary='List all problems',
    status_code=status.HTTP_200_OK,
    response_model=List,
    responses={
        200: {'model': List[ProblemOut]},
        403: {'content': {'application/json': {'example': responses.forbidden_response}}},
        500: {'content': {'application/json': {'example': responses.internal_server_error_response}}},
    },
    tags=['problems'],
)
async def get_problems(
    db: Session = Depends(get_database),
) -> List:
    problems = await get_all(db=db, model=Problem)

    return problems


@problem_router.get(
    '/problems/{id}',
    summary='Get a problem by id',
    status_code=status.HTTP_200_OK,
    response_model=ProblemOut,
    responses={
        200: {'model': ProblemOut},
        403: {'content': {'application/json': {'example': responses.forbidden_response}}},
        404: {'content': {'application/json': {'example': responses.not_found_entity_response}}},
        500: {'content': {'application/json': {'example': responses.internal_server_error_response}}},
    },
    tags=['problems'],
)
async def get_problem(id: UUID, db: Session = Depends(get_database)) -> ProblemOut:
    problem = await get(id=id, db=db, model=Problem)

    return convert_model_to_schema(model=problem)


@problem_router.post(
    '/problems',
    summary='Create a new problem',
    status_code=status.HTTP_201_CREATED,
    response_model=ProblemOut,
    responses={
        201: {'model': ProblemOut},
        403: {'content': {'application/json': {'example': responses.forbidden_response}}},
        404: {'content': {'application/json': {'example': responses.not_found_entity_response}}},
        422: {'content': {'application/json': {'example': responses.unprocessable_entity_response}}},
        500: {'content': {'application/json': {'example': responses.internal_server_error_response}}},
    },
    tags=['problems'],
)
async def create_problem(
    problem: ProblemIn,
    db: Session = Depends(get_database),
) -> ProblemOut:
    try:
        base64_decode(content=problem.data_entry, error_field='data entry')
    except InvalidContent as exc:
        raise RequestValidationError(exc.errors())

    try:
        base64_decode(content=problem.data_output, error_field='data output')
    except InvalidContent as exc:
        raise RequestValidationError(exc.errors())

    try:
        problem_obj = await create(db=db, schema=problem)
    except DuplicateObject:
        # TODO: Return location on headers
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER)

    return convert_model_to_schema(model=problem_obj)


@problem_router.delete(
    '/problems/{id}',
    summary='Delete a problem by id',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'content': {'application/json': {'example': []}}},
        403: {'content': {'application/json': {'example': responses.forbidden_response}}},
        404: {'content': {'application/json': {'example': responses.not_found_entity_response}}},
        409: {'content': {'application/json': {'example': responses.conflict_response}}},
        500: {'content': {'application/json': {'example': responses.internal_server_error_response}}},
    },
    tags=['problems'],
)
async def delete_problem(id: UUID, db: Session = Depends(get_database)) -> None:
    try:
        await delete(id=id, db=db, model=Problem)
    except ConflictObject:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return JSONResponse(content={}, status_code=status.HTTP_204_NO_CONTENT)


@problem_router.put(
    '/problems/{id}',
    summary='Update a problem by id',
    status_code=status.HTTP_200_OK,
    response_model=ProblemOut,
    responses={
        200: {'model': ProblemOut},
        403: {'content': {'application/json': {'example': responses.forbidden_response}}},
        404: {'content': {'application/json': {'example': responses.not_found_entity_response}}},
        500: {'content': {'application/json': {'example': responses.internal_server_error_response}}},
    },
    tags=['problems'],
)
async def update_problem(
    id: UUID,
    problem: ProblemIn,
    db: Session = Depends(get_database),
) -> ProblemOut:
    try:
        problem_obj = await update(id=id, db=db, model=Problem, schema=problem)
    except ConflictObject:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return convert_model_to_schema(model=problem_obj)
