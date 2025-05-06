import uuid
from datetime import datetime, timezone

from fastapi import Depends
from pydantic import UUID4

from src.contrib.exceptions import ObjectNotFound
from src.users.models import UserModel
from src.users.repositories import UserRepository
from src.contrib.hash import HashUtils
from src.users.schemas import (
    UserCollectionResponse,
    UserIn,
    UserOut,
)


class UserUseCase:
    def __init__(
        self,
        repository: UserRepository = Depends(),
    ) -> None:
        self.repository = repository

    async def create(self, user_in: UserIn) -> UserOut:
        user_in.password = HashUtils.hash(user_in.password)
        user_out = UserOut(
            id=str(uuid.uuid4()),
            created_at=datetime.now(timezone.utc),
            **user_in.model_dump(),
        )

        user_model = UserModel(**user_out.model_dump())

        async with await self.repository.start_transaction() as transaction:
            await self.repository.insert(
                model=user_model, session=transaction.session
            )

        return user_out

    async def get(self, id: UUID4) -> UserOut:
        user = await self.repository.get(filter={'id': id})

        if not user:
            raise ObjectNotFound(
                message=f'Object not found on Users for id: {id}'
            )

        return UserOut(**user)

    async def query(self) -> UserCollectionResponse:
        users = await self.repository.query()

        return UserCollectionResponse.create(results=users)
