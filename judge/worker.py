import asyncio
import logging
from datetime import datetime
from typing import Dict, Any
from uuid import UUID

from judge.contrib.rabbitmq import RabbitMQ
from judge.contrib.judge import Judge
from judge.submissions.repositories import SubmissionRepository
from judge.problems.repositories import ProblemRepository
from judge.contrib.repository.mongodb import mongodb_client
from judge.contrib.repository.mongodb_utils import connect_to_mongo, close_mongo_connection
from judge.submissions.schemas import SubmissionOut


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def convert_datetime(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'created_at' and isinstance(value, str):
                obj[key] = datetime.fromisoformat(value)
            elif isinstance(value, (dict, list)):
                convert_datetime(value)
    elif isinstance(obj, list):
        for item in obj:
            convert_datetime(item)


def convert_uuid(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'id' and isinstance(value, str):
                obj[key] = UUID(value)
            elif isinstance(value, (dict, list)):
                convert_uuid(value)
    elif isinstance(obj, list):
        for item in obj:
            convert_uuid(item)


async def process_submission(message: Dict[str, Any]) -> None:
    try:
        convert_datetime(message)
        convert_uuid(message)

        logger.info(f"Received message: {message}")

        if 'submission' not in message or 'problem' not in message:
            logger.error(f"Invalid message format: {message}")
            return

        submission_data = message['submission']
        problem_data = message['problem']

        required_fields = ['id', 'problem_id', 'language_type', 'content', 'status']
        missing_fields = [field for field in required_fields if field not in submission_data]

        if missing_fields:
            logger.error(f"Missing required fields in submission: {missing_fields}")
            logger.error(f"Submission data: {submission_data}")
            return

        submission = SubmissionOut(**submission_data)

        repository = SubmissionRepository(await mongodb_client())
        judge = Judge(repository=repository)

        await judge.process_submission(submission=submission, data=problem_data)
        logger.info(f"Submission {submission.id} processed successfully")
    except Exception as e:
        logger.error(f"Error processing submission: {str(e)}")
        logger.error(f"Message content: {message}")


async def main() -> None:
    await connect_to_mongo()

    rabbitmq = RabbitMQ()
    await rabbitmq.connect()

    logger.info("Worker started. Waiting for submissions...")
    await rabbitmq.consume(process_submission)

    try:
        await asyncio.Future()
    except KeyboardInterrupt:
        logger.info("Worker stopped by user")
    finally:
        await rabbitmq.close()
        await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
