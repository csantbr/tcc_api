from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from apps.problem.model import Problem
from apps.submission.crud import create, delete, get, update
from apps.submission.model import Submission
from apps.submission.schema import SubmissionIn
from contrib import exceptions
from contrib.base64 import decode
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
        raise exceptions.InvalidLanguageType

    if not submission.content:
        raise exceptions.InvalidBase64

    code = decode(submission.content)

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