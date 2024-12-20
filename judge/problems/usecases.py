import uuid
from datetime import datetime, timezone

from fastapi import Depends
from pydantic import UUID4

from judge.contrib.exceptions import ObjectNotFound
from judge.problems.models import ProblemModel
from judge.problems.repositories import ProblemRepository
from judge.problems.schemas import (
    ProblemCollectionResponse,
    ProblemIn,
    ProblemOut,
)


class ProblemUseCase:
    def __init__(
        self,
        repository: ProblemRepository = Depends(),
    ) -> None:
        self.repository = repository

    async def create(self, problem_in: ProblemIn) -> ProblemOut:
        problem_out = ProblemOut(
            id=str(uuid.uuid4()),
            created_at=datetime.now(timezone.utc),
            **problem_in.model_dump(),
        )

        problem_model = ProblemModel(**problem_out.model_dump())

        async with await self.repository.start_transaction() as transaction:
            await self.repository.insert(
                model=problem_model, session=transaction.session
            )

        return problem_out

    async def get(self, id: UUID4) -> ProblemOut:
        problem = await self.repository.get(filter={'id': id})

        if not problem:
            raise ObjectNotFound(
                message=f'Object not found on Problems for id: {id}'
            )

        return ProblemOut(**problem)

    async def query(self) -> ProblemCollectionResponse:
        problems = await self.repository.query()

        return ProblemCollectionResponse.create(results=problems)
