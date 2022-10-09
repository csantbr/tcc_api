from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session

from apps.problems.models import Problem
from apps.submissions.crud import create, delete, get, update
from apps.submissions.models import Submission
from apps.submissions.schemas import SubmissionIn
from contrib.base64 import decode
from contrib.exceptions import InvalidBase64, InvalidLanguageType
from contrib.judge import judge_submission
from database.session import Base, engine, get_database

Base.metadata.create_all(bind=engine)

submission_router = APIRouter()


@submission_router.get('/submissions', status_code=status.HTTP_200_OK, tags=['submissions'])
async def get_submissions(db: Session = Depends(get_database)):
    submissions = await get(db=db, model=Submission)

    return submissions


@submission_router.get('/submissions/{id}', status_code=status.HTTP_200_OK, tags=['submissions'])
async def get_submission(id: UUID, db: Session = Depends(get_database)):
    submission = await get(id=id, db=db, model=Submission)

    return submission


@submission_router.post('/submissions', status_code=status.HTTP_201_CREATED, tags=['submissions'])
async def create_submission(
    submission: SubmissionIn, background_tasks: BackgroundTasks, db: Session = Depends(get_database)
):
    if submission.language_type not in ['py', 'c', 'cpp']:
        exception = InvalidLanguageType(error_field='language_type')
        raise RequestValidationError(exception.errors())

    if not submission.content:
        exception = InvalidBase64(error_field='content')
        raise RequestValidationError(exception.errors())

    try:
        code = decode(submission.content)
    except InvalidBase64 as exc:
        raise RequestValidationError(exc.errors())

    problem_obj = await get(db=db, model=Problem, id=submission.problem_id)
    submission_obj = await create(db=db, schema=submission)

    background_tasks.add_task(
        judge_submission,
        id=submission_obj.id,
        code=code,
        collection=problem_obj,
        schema=submission,
        db=db,
    )

    return submission


@submission_router.delete('/submissions/{id}', status_code=status.HTTP_200_OK, tags=['submissions'])
async def delete_submission(id: UUID, db: Session = Depends(get_database)):
    await delete(id=id, db=db, model=Submission)

    return {'status': 'submission deleted'}


@submission_router.patch('/submissions/{id}', status_code=status.HTTP_200_OK, tags=['submissions'])
async def update_submission(id: UUID, submission: SubmissionIn, db: Session = Depends(get_database)):
    await update(id=id, db=db, model=Submission, schema=submission)

    return {'status': 'submission updated'}
