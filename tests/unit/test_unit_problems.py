
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.problems.usecases import ProblemUseCase
from src.problems.schemas import ProblemIn, ProblemOut, ProblemUpdate, ProblemCollectionResponse
import uuid
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_create_problem():
    problem_data = ProblemIn(
        name="Test Problem",
        description="Test Description",
        entry_description="Test Entry Description",
        output_description="Test Output Description"
    )
    
    mock_problem_repository = MagicMock()
    
    async def start_transaction():
        return AsyncMock()
    
    mock_problem_repository.start_transaction = start_transaction
    mock_problem_repository.insert = AsyncMock()
    
    problem_use_case = ProblemUseCase(repository=mock_problem_repository)
    await problem_use_case.create(problem_in=problem_data)
    
    mock_problem_repository.insert.assert_called_once()

@pytest.mark.asyncio
async def test_get_problem():
    problem_id = uuid.uuid4()
    problem_data = {
        "id": problem_id,
        "name": "Test Problem",
        "description": "Test Description",
        "entry_description": "Test Entry Description",
        "output_description": "Test Output Description",
        "created_at": datetime.now(timezone.utc)
    }

    mock_problem_repository = MagicMock()
    mock_problem_repository.get = AsyncMock(return_value=problem_data)

    problem_use_case = ProblemUseCase(repository=mock_problem_repository)
    problem = await problem_use_case.get(id=problem_id)

    mock_problem_repository.get.assert_called_once_with(filter={'id': problem_id})
    assert isinstance(problem, ProblemOut)
    assert problem.id == problem_id

@pytest.mark.asyncio
async def test_query_problems():
    problem_list = [
        {
            "id": uuid.uuid4(),
            "name": "Test Problem 1",
            "description": "Test Description 1",
            "entry_description": "Test Entry Description 1",
            "output_description": "Test Output Description 1",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "id": uuid.uuid4(),
            "name": "Test Problem 2",
            "description": "Test Description 2",
            "entry_description": "Test Entry Description 2",
            "output_description": "Test Output Description 2",
            "created_at": datetime.now(timezone.utc)
        }
    ]

    mock_problem_repository = MagicMock()
    mock_problem_repository.query = AsyncMock(return_value=problem_list)

    problem_use_case = ProblemUseCase(repository=mock_problem_repository)
    problems_response = await problem_use_case.query()

    mock_problem_repository.query.assert_called_once()
    assert isinstance(problems_response, ProblemCollectionResponse)
    assert len(problems_response.results) == 2

@pytest.mark.asyncio
async def test_update_problem():
    problem_id = uuid.uuid4()
    problem_data = {
        "id": problem_id,
        "name": "Test Problem",
        "description": "Test Description",
        "entry_description": "Test Entry Description",
        "output_description": "Test Output Description",
        "created_at": datetime.now(timezone.utc)
    }
    problem_update_data = ProblemUpdate(name="Updated Problem")

    mock_problem_repository = MagicMock()
    mock_problem_repository.get = AsyncMock(return_value=problem_data)
    
    async def start_transaction():
        return AsyncMock()
    
    mock_problem_repository.start_transaction = start_transaction
    mock_problem_repository.update = AsyncMock()

    problem_use_case = ProblemUseCase(repository=mock_problem_repository)
    updated_problem = await problem_use_case.update(id=problem_id, problem_in=problem_update_data)

    mock_problem_repository.get.assert_called_once_with(filter={'id': problem_id})
    mock_problem_repository.update.assert_called_once()
    assert updated_problem.name == "Updated Problem"
    assert updated_problem.id == problem_id
    assert updated_problem.updated_at is not None
