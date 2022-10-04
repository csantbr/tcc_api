from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.problems.crud import create, delete, get, update
from apps.problems.models import Problem
from apps.problems.schemas import ProblemIn
from contrib.exceptions import DuplicatedObject
from database.session import Base, engine, get_database

Base.metadata.create_all(bind=engine)

problem_router = APIRouter()


@problem_router.get('/problems', status_code=status.HTTP_200_OK, tags=['problems'])
async def get_problems(
    db: Session = Depends(get_database),
):
    problems = await get(db=db, model=Problem)

    return problems


@problem_router.get('/problems/{id}', status_code=status.HTTP_200_OK, tags=['problems'])
async def get_problem(
    id: UUID,
    db: Session = Depends(get_database),
):
    problem = await get(id=id, db=db, model=Problem)

    return problem


@problem_router.post('/problems', status_code=status.HTTP_201_CREATED, tags=['problems'])
async def create_problem(
    problem: ProblemIn,
    db: Session = Depends(get_database),
):
    try:
        await create(db=db, schema=problem)
    except DuplicatedObject:
        # TODO: Return location on headers
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER)

    return problem


@problem_router.delete('/problems/{id}', status_code=status.HTTP_200_OK, tags=['problems'])
async def delete_problem(
    id: UUID,
    db: Session = Depends(get_database),
):
    await delete(id=id, db=db, model=Problem)

    return {'status': 'problem deleted'}


@problem_router.patch('/problems/{id}', status_code=status.HTTP_200_OK, tags=['problems'])
async def update_problem(
    id: UUID,
    problem: ProblemIn,
    db: Session = Depends(get_database),
):
    await update(id=id, db=db, model=Problem, schema=problem)

    return {'status': 'problem updated'}
