from database.session import Base
from fastapi import APIRouter, Body, status, Depends, Form
from database.session import engine, get_database
from sqlalchemy.orm import Session
from models.submission import Submission as SubmissionModel
from schemas.submission import Submission
from crud import get, delete, update
from uuid import UUID
from contrib.judge import judge_submission

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
async def create_submission(submission: Submission, db: Session = Depends(get_database)):
    await judge_submission(db=db, schema=submission)

    return submission


@submission_router.delete('/submissions/{id}', status_code=status.HTTP_200_OK, tags=['submissions'])
async def delete_submission(id: UUID, db: Session = Depends(get_database)):
    await delete(id=id, db=db, model=SubmissionModel)

    return {'status': 'submission deleted'}


@submission_router.patch('/submissions/{id}', status_code=status.HTTP_200_OK, tags=['submissions'])
async def update_submission(id: UUID, submission: Submission, db: Session = Depends(get_database)):
    await update(id=id, db=db, model=SubmissionModel, schema=submission)

    return {'status': 'submission updated'}
