import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from starlette.testclient import TestClient

from config import settings
from main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        client.headers = {'Authorization': f'Bearer {settings.BEARER_KEY}'}
        yield client
