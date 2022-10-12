from typing import Any, List
from uuid import UUID

from sqlalchemy.orm import Session

from apps.submissions.models import Submission
from apps.submissions.schemas import SubmissionIn
from contrib.exceptions import NotFoundException
from converters.schemas import convert_schema_to_model


async def get(db: Session, id: UUID, model: Submission) -> Submission:
    query = db.query(model).filter(model.id == id).first()

    if not query:
        raise NotFoundException

    return query


async def get_all(db: Session, model: Submission) -> List[Submission]:
    query = db.query(model).all()

    return query


async def create(db: Session, schema: SubmissionIn):
    query = convert_schema_to_model(schema=schema)

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
