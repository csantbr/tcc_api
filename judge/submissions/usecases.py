import uuid
import logging
from datetime import datetime, timezone

from fastapi import Depends
from pydantic import UUID4

from judge.contrib.constants import SUPPORTED_LANGUAGES
from judge.submissions.models import SubmissionModel
from judge.submissions.repositories import SubmissionRepository
from judge.problems.repositories import ProblemRepository
from judge.contrib.exceptions import ObjectNotFound, ValidationError
from judge.contrib.base64 import Base64Utils
from judge.contrib.judge import Judge
from judge.contrib.rabbitmq import RabbitMQ
from judge.submissions.schemas import (
    SubmissionCollectionResponse,
    SubmissionIn,
    SubmissionOut,
)

logger = logging.getLogger(__name__)


class SubmissionUseCase:
    def __init__(
        self,
        repository: SubmissionRepository = Depends(),
        problem_repository: ProblemRepository = Depends(),
    ) -> None:
        self.repository = repository
        self.problem_repository = problem_repository
        self.judge = Judge(repository=repository)
        self.rabbitmq = RabbitMQ()

    async def create(self, submission_in: SubmissionIn) -> SubmissionOut:
        problem = await self.problem_repository.get(
            filter={'id': submission_in.problem_id}
        )
        if not problem:
            raise ObjectNotFound()

        if submission_in.language_type not in SUPPORTED_LANGUAGES:
            raise ValidationError(
                message='Invalid language type', field='language_type'
            )

        if not Base64Utils.is_valid(submission_in.content):
            raise ValidationError(
                message='Invalid content, the content must be a valid base64.', field='content'
            )

        submission_out = SubmissionOut(
            id=str(uuid.uuid4()),
            created_at=datetime.now(timezone.utc),
            status='PENDING',
            **submission_in.model_dump(),
        )

        submission_model = SubmissionModel(**submission_out.model_dump())

        async with await self.repository.start_transaction() as transaction:
            await self.repository.insert(
                model=submission_model, session=transaction.session
            )

        submission_dict = submission_out.model_dump()
        logger.info(f"Sending submission to queue: {submission_dict}")

        await self.rabbitmq.publish({
            'submission': submission_dict,
            'problem': problem
        })

        return submission_out

    async def get(self, id: UUID4) -> SubmissionOut:
        submission = await self.repository.get(filter={'id': id})

        if not submission:
            raise ObjectNotFound(
                message=f'Object not found on Submissions for id: {id}'
            )

        return SubmissionOut(**submission)

    async def query(self) -> SubmissionCollectionResponse:
        submissions = await self.repository.query()

        return SubmissionCollectionResponse.create(results=submissions)
