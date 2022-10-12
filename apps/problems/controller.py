from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.problems.crud import create, delete, get, update
from apps.problems.models import Problem
from apps.problems.schemas import ProblemIn, ProblemOut
from contrib.exceptions import DuplicateObject
from database.session import Base, engine, get_database
from converters.schemas import convert_model_to_schema

Base.metadata.create_all(bind=engine)

problem_router = APIRouter()


@problem_router.get('/problems', summary='List all problems', status_code=status.HTTP_200_OK, tags=['problems'])
async def get_problems(
    db: Session = Depends(get_database),
):
    problems = await get(db=db, model=Problem)

    return problems


@problem_router.get('/problems/{id}', summary='Get a problem by id', status_code=status.HTTP_200_OK, response_model=ProblemOut, tags=['problems'])
async def get_problem(
    id: UUID,
    db: Session = Depends(get_database),
):
    problem = await get(id=id, db=db, model=Problem)
    
    return problem


@problem_router.post('/problems', summary='Create a new problem', status_code=status.HTTP_201_CREATED, response_model=ProblemOut, tags=['problems'])
async def create_problem(
    problem: ProblemIn,
    db: Session = Depends(get_database),
) -> ProblemOut:
    try:
        problem_obj = await create(db=db, schema=problem)
    except DuplicateObject:
        # TODO: Return location on headers
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER)

    return convert_model_to_schema(model=problem_obj)


@problem_router.delete('/problems/{id}', summary='Delete a problem by id', status_code=status.HTTP_200_OK, tags=['problems'])
async def delete_problem(
    id: UUID,
    db: Session = Depends(get_database),
) -> None:
    await delete(id=id, db=db, model=Problem)

    return {'status': 'problem deleted'}


@problem_router.patch('/problems/{id}', summary='Update a problem by id', status_code=status.HTTP_200_OK, tags=['problems'])
async def update_problem(
    id: UUID,
    problem: ProblemIn,
    db: Session = Depends(get_database),
) -> str:
    await update(id=id, db=db, model=Problem, schema=problem)

    return {'status': 'problem updated'}
