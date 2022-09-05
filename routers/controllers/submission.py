from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.exceptions import HTTPException, RequestValidationError
from pydantic.error_wrappers import ErrorWrapper
from sqlalchemy.orm import Session

from contrib.exceptions import InvalidBase64
from contrib.judge import judge_submission
from crud import create, delete, get, update
from database.session import Base, engine, get_database
from models.submission import Submission as SubmissionModel
from routers.controllers.problem import get_problem
from schemas.submission import Submission

Base.metadata.create_all(bind=engine)

submission_router = APIRouter()


@submission_router.get('/submissions', status_code=status.HTTP_200_OK, tags=['submissions'])
async def get_submissions(db: Session = Depends(get_database)):
    submissions = await get(db=db, model=SubmissionModel)

    return submissions


@submission_router.get('/submissions/{id}', status_code=status.HTTP_200_OK, tags=['submissions'])
async def get_submission(id: UUID, db: Session = Depends(get_database)):
    submission = await get(id=id, db=db, model=SubmissionModel)

    return submission


@submission_router.post('/submissions', status_code=status.HTTP_201_CREATED, tags=['submissions'])
async def create_submission(
    submission: Submission, background_tasks: BackgroundTasks, db: Session = Depends(get_database)
):
    submission_obj = await create(db=db, schema=submission)
    problem_obj = await get_problem(id=submission.problem_id, db=db)

    background_tasks.add_task(judge_submission, id=submission_obj.id, collection=problem_obj, schema=submission, db=db)

    return submission


@submission_router.delete('/submissions/{id}', status_code=status.HTTP_200_OK, tags=['submissions'])
async def delete_submission(id: UUID, db: Session = Depends(get_database)):
    await delete(id=id, db=db, model=SubmissionModel)

    return {'status': 'submission deleted'}


@submission_router.patch('/submissions/{id}', status_code=status.HTTP_200_OK, tags=['submissions'])
async def update_submission(id: UUID, submission: Submission, db: Session = Depends(get_database)):
    await update(id=id, db=db, model=SubmissionModel, schema=submission)

    return {'status': 'submission updated'}
