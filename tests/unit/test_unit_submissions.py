
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.submissions.usecases import SubmissionUseCase
from src.submissions.schemas import SubmissionIn, SubmissionOut, SubmissionCollectionResponse
from src.problems.schemas import ProblemOut
import uuid
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_create_submission():
    problem_id = uuid.uuid4()
    submission_data = SubmissionIn(
        problem_id=problem_id,
        language_type="py",
        content="ZGVmIG1haW4oKToKICAgIHBhc3M="
    )
    
    mock_submission_repository = MagicMock()
    mock_problem_repository = MagicMock()
    
    async def start_transaction():
        return AsyncMock()
    
    mock_submission_repository.start_transaction = start_transaction
    mock_submission_repository.insert = AsyncMock()
    
    mock_problem_repository.get = AsyncMock(return_value=ProblemOut(
        id=problem_id,
        name="Test Problem",
        description="Test Description",
        entry_description="Test Entry Description",
        output_description="Test Output Description",
        created_at=datetime.now(timezone.utc)
    ))

    with patch('src.submissions.usecases.queue_manager') as mock_queue_manager:
        submission_use_case = SubmissionUseCase(
            repository=mock_submission_repository, 
            problem_repository=mock_problem_repository
        )
        await submission_use_case.create(submission_in=submission_data)
        
        mock_submission_repository.insert.assert_called_once()
        mock_queue_manager.enqueue.assert_called_once()

@pytest.mark.asyncio
async def test_get_submission():
    submission_id = uuid.uuid4()
    problem_id = uuid.uuid4()
    submission_data = {
        "id": submission_id,
        "problem_id": problem_id,
        "language_type": "py",
        "content": "ZGVmIG1haW4oKToKICAgIHBhc3M=",
        "status": "PENDING",
        "created_at": datetime.now(timezone.utc)
    }

    mock_submission_repository = MagicMock()
    mock_submission_repository.get = AsyncMock(return_value=submission_data)

    submission_use_case = SubmissionUseCase(repository=mock_submission_repository, problem_repository=MagicMock())
    submission = await submission_use_case.get(id=submission_id)

    mock_submission_repository.get.assert_called_once_with(filter={'id': submission_id})
    assert isinstance(submission, SubmissionOut)
    assert submission.id == submission_id

@pytest.mark.asyncio
async def test_query_submissions():
    submission_list = [
        {
            "id": uuid.uuid4(),
            "problem_id": uuid.uuid4(),
            "language_type": "py",
            "content": "ZGVmIG1haW4oKToKICAgIHBhc3M=",
            "status": "PENDING",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "id": uuid.uuid4(),
            "problem_id": uuid.uuid4(),
            "language_type": "py",
            "content": "ZGVmIG1haW4oKToKICAgIHBhc3M=",
            "status": "ACCEPTED",
            "created_at": datetime.now(timezone.utc)
        }
    ]

    mock_submission_repository = MagicMock()
    mock_submission_repository.query = AsyncMock(return_value=submission_list)

    submission_use_case = SubmissionUseCase(repository=mock_submission_repository, problem_repository=MagicMock())
    submissions_response = await submission_use_case.query()

    mock_submission_repository.query.assert_called_once()
    assert isinstance(submissions_response, SubmissionCollectionResponse)
    assert len(submissions_response.results) == 2
