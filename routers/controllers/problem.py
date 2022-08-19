from fastapi import APIRouter, status, Depends
from database.session import Base, engine, get_database
from sqlalchemy.orm import Session
from models.problem import Problem as ProblemModel
from schemas.problem import Problem
from crud import get, create, delete, update
from uuid import UUID

Base.metadata.create_all(bind=engine)

problem_router = APIRouter()


@problem_router.get('/problems', status_code=status.HTTP_200_OK, tags=['problems'])
async def get_problems(
    db: Session = Depends(get_database),
):
    problems = await get(db=db, model=ProblemModel)

    return problems


@problem_router.get('/problems/{id}', status_code=status.HTTP_200_OK, tags=['problems'])
async def get_problem(
    id: UUID,
    db: Session = Depends(get_database),
):
    problem = await get(id=id, db=db, model=ProblemModel)

    return problem


@problem_router.post('/problems', status_code=status.HTTP_201_CREATED, tags=['problems'])
async def create_problem(
    problem: Problem,
    db: Session = Depends(get_database),
):
    await create(db=db, schema=problem)

    return problem


@problem_router.delete('/problems/{id}', status_code=status.HTTP_200_OK, tags=['problems'])
async def delete_problem(
    id: UUID,
    db: Session = Depends(get_database),
):
    await delete(id=id, db=db, model=ProblemModel)

    return {'status': 'problem deleted'}


@problem_router.patch('/problems/{id}', status_code=status.HTTP_200_OK, tags=['problems'])
async def update_problem(
    id: UUID,
    problem: Problem,
    db: Session = Depends(get_database),
):
    await update(id=id, db=db, model=ProblemModel, schema=problem)

    return {'status': 'problem updated'}
