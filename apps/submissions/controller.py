from typing import List
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Body, Depends, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from apps.problems.models import Problem
from apps.submissions.crud import create, delete, get, get_all
from apps.submissions.models import Submission
from apps.submissions.schemas import SubmissionIn, SubmissionOut
from contrib import responses
from contrib.exceptions import InvalidContent, InvalidLanguageType
from contrib.helpers import base64_decode, valid
from contrib.judge import judge_submission
from converters.schemas import convert_model_to_schema
from database.session import Base, engine, get_database

Base.metadata.create_all(bind=engine)

submission_router = APIRouter()


@submission_router.get(
    '/submissions',
    summary='List all submissions',
    status_code=status.HTTP_200_OK,
    response_model=List,
    responses={
        200: {'model': List[SubmissionOut]},
        403: {'content': {'application/json': {'example': responses.forbidden_response}}},
        500: {'content': {'application/json': {'example': responses.internal_server_error_response}}},
    },
    tags=['submissions'],
)
async def get_submissions(db: Session = Depends(get_database)) -> List:
    submissions = await get_all(db=db, model=Submission)

    return submissions


@submission_router.get(
    '/submissions/{id}',
    summary='Get a submission by id',
    status_code=status.HTTP_200_OK,
    response_model=SubmissionOut,
    responses={
        200: {'model': SubmissionOut},
        403: {'content': {'application/json': {'example': responses.forbidden_response}}},
        404: {'content': {'application/json': {'example': responses.not_found_entity_response}}},
        500: {'content': {'application/json': {'example': responses.internal_server_error_response}}},
    },
    tags=['submissions'],
)
async def get_submission(id: UUID, db: Session = Depends(get_database)) -> SubmissionOut:
    submission = await get(id=id, db=db, model=Submission)

    return convert_model_to_schema(model=submission)


@submission_router.post(
    '/submissions',
    summary='Send a new submission',
    status_code=status.HTTP_201_CREATED,
    response_model=SubmissionOut,
    responses={
        201: {'model': SubmissionOut},
        403: {'content': {'application/json': {'example': responses.forbidden_response}}},
        404: {'content': {'application/json': {'example': responses.not_found_entity_response}}},
        422: {'content': {'application/json': {'example': responses.unprocessable_entity_response}}},
        500: {'content': {'application/json': {'example': responses.internal_server_error_response}}},
    },
    tags=['submissions'],
)
async def create_submission(
    background_tasks: BackgroundTasks, submission_in: SubmissionIn = Body(...), db: Session = Depends(get_database)
) -> SubmissionOut:
    problem_obj = await get(db=db, model=Problem, id=submission_in.problem_id)

    try:
        valid(submission_in.language_type)
    except InvalidLanguageType as exc:
        raise RequestValidationError(exc.errors())

    try:
        code = base64_decode(submission_in.content)
    except InvalidContent as exc:
        raise RequestValidationError(exc.errors())

    submission_obj = await create(db=db, schema=submission_in)

    background_tasks.add_task(
        judge_submission,
        id=submission_obj.id,
        code=code,
        collection=problem_obj,
        schema=submission_in,
        db=db,
    )

    return convert_model_to_schema(model=submission_obj)


@submission_router.delete(
    '/submissions/{id}',
    summary='Delete a submission by id',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {'content': {'application/json': {'example': []}}},
        403: {'content': {'application/json': {'example': responses.forbidden_response}}},
        404: {'content': {'application/json': {'example': responses.not_found_entity_response}}},
        500: {'content': {'application/json': {'example': responses.internal_server_error_response}}},
    },
    tags=['submissions'],
)
async def delete_submission(id: UUID, db: Session = Depends(get_database)) -> None:
    await delete(id=id, db=db, model=Submission)

    return JSONResponse(content={}, status_code=status.HTTP_204_NO_CONTENT)
