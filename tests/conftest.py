import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from starlette.testclient import TestClient

from config import settings
from database.session import Base, engine
from main import app


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        client.headers = {'Authorization': f'Bearer {settings.BEARER_KEY}'}
        yield client


@pytest.fixture
def problem_data():
    return {
        'name': 'example',
        'description': 'example description',
        'data_entry': 'example data_entry',
        'entry_description': 'example entry_description',
        'data_output': 'example data_output',
        'output_description': 'example output_description',
    }


@pytest.fixture
def database_problem(client, problem_data):
    problem_obj = client.post('/api/problems', json=problem_data)
    return problem_obj
