from sqlalchemy.orm import Session
from typing import TypeVar, List, Any
from contrib.exceptions import NotFoundException
from converters.schemas import convert_schema_to_model, set_schema_to_model


TModel = TypeVar('TModel')
TSchema = TypeVar('TSchema')


async def get(db: Session, model: TModel, id: Any = None) -> List[TModel]:
    if id:
        query = db.query(model).filter(model.id == id).first()

        if not query:
            raise NotFoundException
    else:
        query = db.query(model).all()

    return query


async def create(db: Session, schema: TSchema) -> None:
    query = convert_schema_to_model(schema=schema)

    db.add(query)
    db.commit()


async def update(db: Session, model: TModel, schema: TSchema, id: Any = None) -> None:
    user_model = await get(id=id, db=db, model=model)

    query = set_schema_to_model(schema=schema, model=user_model)

    db.add(query)
    db.commit()


async def delete(db: Session, model: TModel, id: Any = None) -> None:
    query = db.query(model).filter(model.id == id).first()

    if not query:
        raise NotFoundException

    db.query(model).filter(model.id == id).delete()
    db.commit()
