import os
import sys
import pytest
from base64 import b64encode

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI

from config import settings
from apps.problems.examples import problem_in_complete
from apps.submissions.examples import submission_in_complete
from contrib.exceptions import DuplicateObject, InvalidContent

app = FastAPI()


def test_get_should_return_success(client):
    response = client.get('/api/problems')
    assert response.status_code == 200


def test_get_should_fail_with_invalid_authorization_(client):
    client.headers = {'Authorization': f'Bearer fake'}

    response = client.get('/api/problems')
    assert response.status_code == 403


def test_post_should_return_sucess_with_valid_payload(client):
    problem_in_complete['name'] = 'Teste'
    problem_in_complete['data_entry'] = 'ZXhlbXBsbw=='
    response = client.post('/api/problems', json=problem_in_complete)
    breakpoint()
    
    assert response.status_code == 201


def test_post_should_return_see_other(client):
    problem_in_complete['data_entry'] = 'ZXhlbXBsbw=='
    response = client.post('/api/problems', json=problem_in_complete)

    assert response.status_code == 303
    assert response.json()['detail'] == 'See Other'


def test_post_should_return_unprocessable_entity_with_invalid_data_entry(client):
    response = client.post('/api/problems', json=problem_in_complete)

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Invalid data entry, the data entry must be a valid base64.'


def test_post_should_return_not_found_with_invalid_problem_id(client):
    response = client.post('/api/submissions', json=submission_in_complete)

    assert response.status_code == 404
    assert response.json()['detail'] == 'Not found'


def test_post_should_return_not_found_with_invalid_problem_id(client):
    submission_in_complete['language_type'] = 'java'
    response = client.post('/api/submissions', json=submission_in_complete)

    assert response.status_code == 404
    assert response.json()['detail'] == 'Not found'