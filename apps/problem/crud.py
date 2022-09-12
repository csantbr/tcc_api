from typing import Any, List, TypeVar

from sqlalchemy.orm import Session

from apps.problem.model import Problem
from apps.problem.schema import ProblemIn
from contrib.exceptions import NotFoundException
from converters.schemas import convert_schema_to_model, set_schema_to_model


async def get(db: Session, model: Problem, id: Any = None) -> List[Problem]:
    if id:
        query = db.query(model).filter(model.id == id).first()

        if not query:
            raise NotFoundException
    else:
        query = db.query(model).all()

    return query


async def create(db: Session, schema: ProblemIn):
    query = convert_schema_to_model(schema=schema)

    db.add(query)
    db.commit()

    return query


async def update(db: Session, model: Problem, schema: ProblemIn, id: Any = None):
    user_model = await get(id=id, db=db, model=model)

    query = set_schema_to_model(schema=schema, model=user_model)

    db.add(query)
    db.commit()

    return query


async def delete(db: Session, model: Problem, id: Any = None):
    query = db.query(model).filter(model.id == id).first()

    if not query:
        raise NotFoundException

    db.query(model).filter(model.id == id).delete()
    db.commit()

    return query