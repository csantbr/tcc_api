
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.users.usecases import UserUseCase
from src.users.schemas import UserIn, UserOut, UserCollectionResponse
import uuid
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_create_user():
    user_data = UserIn(username="testuser", password="password")
    
    mock_user_repository = MagicMock()
    
    async def start_transaction():
        return AsyncMock()
    
    mock_user_repository.start_transaction = start_transaction
    mock_user_repository.insert = AsyncMock()
    
    user_use_case = UserUseCase(repository=mock_user_repository)
    await user_use_case.create(user_in=user_data)
    
    mock_user_repository.insert.assert_called_once()

@pytest.mark.asyncio
async def test_get_user():
    user_id = uuid.uuid4()
    user_data = {
        "id": user_id,
        "username": "testuser",
        "password": "password",
        "role": "PARTICIPANT",
        "created_at": datetime.now(timezone.utc)
    }

    mock_user_repository = MagicMock()
    mock_user_repository.get = AsyncMock(return_value=user_data)

    user_use_case = UserUseCase(repository=mock_user_repository)
    user = await user_use_case.get(id=user_id)

    mock_user_repository.get.assert_called_once_with(filter={'id': user_id})
    assert isinstance(user, UserOut)
    assert user.id == user_id

@pytest.mark.asyncio
async def test_query_users():
    user_list = [
        {
            "id": uuid.uuid4(),
            "username": "testuser1",
            "password": "password",
            "role": "PARTICIPANT",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "id": uuid.uuid4(),
            "username": "testuser2",
            "password": "password",
            "role": "PARTICIPANT",
            "created_at": datetime.now(timezone.utc)
        }
    ]

    mock_user_repository = MagicMock()
    mock_user_repository.query = AsyncMock(return_value=user_list)

    user_use_case = UserUseCase(repository=mock_user_repository)
    users_response = await user_use_case.query()

    mock_user_repository.query.assert_called_once()
    assert isinstance(users_response, UserCollectionResponse)
    assert len(users_response.results) == 2
