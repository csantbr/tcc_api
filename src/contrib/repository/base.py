from functools import cached_property
from typing import Any, Optional

import pymongo
from bson import ObjectId
from motor.core import AgnosticClient, AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorClientSession
from pydantic import BaseModel

from src.contrib.repository.exceptions import DuplicateKeyError


class Transaction:
    def __init__(self, session: AgnosticClient) -> None:
        self.session = session

    async def abort(self) -> None:
        await self.session.abort_transaction()

    async def commit(self) -> None:
        await self.session.commit_transaction()

    def start_transaction(self) -> None:
        self.session.start_transaction()

    async def close(self) -> None:
        await self.session.end_session()

    async def __aenter__(self) -> 'Transaction':
        self.start_transaction()
        return self

    async def __aexit__(self, exc_t: Any, exc_v: Any, exc_tb: Any) -> None:
        try:
            if exc_v:
                await self.abort()
            else:
                await self.commit()
        finally:
            await self.close()

    async def insert(self, model: BaseModel) -> tuple[ObjectId, bool]:
        payload = model.model_dump(by_alias=True)
        try:
            result = await self.storage.insert_one(payload, session=self.session)
        except pymongo.errors.DuplicateKeyError:
            raise DuplicateKeyError()
        return result.inserted_id, result.acknowledged


class Repository:
    storage_name: str

    def __init__(self, client: AgnosticClient) -> None:
        self.client = client

    @cached_property
    def storage(self) -> AgnosticCollection:
        database = self.client.get_default_database()
        return database[self.storage_name]

    async def _start_session(self) -> AsyncIOMotorClientSession:
        return await self.client.start_session()

    async def start_transaction(self) -> Transaction:
        session = await self._start_session()
        return Transaction(session=session)

    async def insert(self, model: BaseModel, session: Optional[AsyncIOMotorClientSession] = None) -> tuple[ObjectId, bool]:
        payload = model.model_dump(by_alias=True)
        try:
            result = await self.storage.insert_one(payload, session=session)
        except pymongo.errors.DuplicateKeyError as exc:
            raise DuplicateKeyError(str(exc))
        return result.inserted_id, result.acknowledged

    async def count(self, filter: Optional[dict[str, Any]] = None) -> int:
        return await self.storage.count_documents(filter=filter or {})

    async def exists(self, filter: Optional[dict[str, Any]] = None) -> bool:
        return await self.count(filter=filter) > 0

    async def get(self, filter: Optional[dict[str, Any]] = None, fields: Optional[dict[str, bool]] = None) -> dict[str, Any]:
        result = await self.storage.find_one(filter or {}, fields)
        if result:
            result.pop('_id', None)
        return result or {}

    async def query(self, filter: Optional[dict[str, Any]] = None, fields: Optional[dict[str, bool]] = None) -> list[dict[str, Any]]:
        results = [cur async for cur in self.storage.find(filter or {}, fields)]
        return [{k: v for k, v in result.items() if k != '_id'} for result in results]

    async def delete(self, filter: dict[str, Any], session: Optional[AsyncIOMotorClientSession] = None) -> bool:
        result = await self.storage.delete_one(filter=filter, session=session)
        return result.deleted_count > 0

    async def update(self, data: dict[str, Any], filter: Optional[dict[str, Any]] = None, upsert: bool = False, session: Optional[AsyncIOMotorClientSession] = None) -> tuple[int, bool]:
        result = await self.storage.update_one(filter or {}, {'$set': data}, upsert=upsert, session=session)
        return result.modified_count, result.acknowledged
