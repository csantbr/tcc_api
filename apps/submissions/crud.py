from typing import Any, List

from sqlalchemy.orm import Session

from apps.submissions.models import Submission
from apps.submissions.schemas import SubmissionIn
from contrib.exceptions import NotFoundException
from converters.schemas import convert_schema_to_model, set_schema_to_model


async def get(db: Session, model: Submission, id: Any = None) -> List[Submission]:
    if id:
        query = db.query(model).filter(model.id == id).first()

        if not query:
            raise NotFoundException
    else:
        query = db.query(model).all()

    return query


async def create(db: Session, schema: SubmissionIn):
    query = convert_schema_to_model(schema=schema)

    db.add(query)
    db.commit()

    return query


async def update(db: Session, model: Submission, schema: SubmissionIn, id: Any = None):
    _model = await get(id=id, db=db, model=model)

    query = set_schema_to_model(schema=schema, model=_model)

    db.add(query)
    db.commit()

    return query


async def delete(db: Session, model: Submission, id: Any = None):
    query = db.query(model).filter(model.id == id).first()

    if not query:
        raise NotFoundException

    db.query(model).filter(model.id == id).delete()
    db.commit()

    return query
