from typing import List
from uuid import UUID

import sqlalchemy
from sqlalchemy.orm import Session

from apps.problems.models import Problem
from apps.problems.schemas import ProblemIn
from contrib.exceptions import ConflictObject, DuplicateObject, NotFoundException
from converters.schemas import convert_schema_to_model, set_schema_to_model


async def get(db: Session, id: UUID, model: Problem) -> Problem:
    query = db.query(model).filter(model.id == id).first()

    if not query:
        raise NotFoundException

    return query


async def get_all(db: Session, model: Problem) -> List[Problem]:
    query = db.query(model).all()

    return query


async def create(db: Session, schema: ProblemIn):
    query = convert_schema_to_model(schema=schema)

    try:
        db.add(query)
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise DuplicateObject(message=f'There is already a problem with this name: {schema.name}')

    return query


async def update(db: Session, id: UUID, model: Problem, schema: ProblemIn):
    model = await get(id=id, db=db, model=model)

    query = set_schema_to_model(schema=schema, model=model)

    try:
        db.add(query)
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise ConflictObject()

    return query


async def delete(db: Session, id: UUID, model: Problem):
    query = db.query(model).filter(model.id == id).first()

    if not query:
        raise NotFoundException

    try:
        db.query(model).filter(model.id == id).delete()
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise ConflictObject()

    return query
