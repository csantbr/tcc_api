import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ast import literal_eval

from fastapi import FastAPI

from apps.submissions.examples import submission_in_complete

app = FastAPI()


def test_get_should_return_success(client):
    response = client.get('/api/problems')
    assert response.status_code == 200


def test_get_should_fail_with_invalid_authorization_(client):
    client.headers = {'Authorization': f'Bearer fake'}

    response = client.get('/api/problems')
    assert response.status_code == 403


def test_post_should_return_success(database_problem):
    assert database_problem.status_code == 201


def test_post_should_return_success(database_problem):
    assert database_problem.status_code == 201


def test_post_should_return_see_other(client, database_problem, problem_data):
    response = client.post('/api/problems', json=problem_data)

    assert response.status_code == 303
    assert response.json()['detail'] == 'See Other'


def test_post_should_return_unprocessable_entity_with_invalid_data_entry(client, problem_data):
    problem_data['data_entry'] = 'example'
    response = client.post('/api/problems', json=problem_data)

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Invalid data entry, the data entry must be a valid base64.'


def test_post_should_return_see_other(client, database_problem, problem_data):
    response = client.post('/api/problems', json=problem_data)

    assert response.status_code == 303
    assert response.json()['detail'] == 'See Other'


def test_post_should_return_unprocessable_entity_with_invalid_data_entry(client, problem_data):
    problem_data['data_entry'] = 'example'
    response = client.post('/api/problems', json=problem_data)

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Invalid data entry, the data entry must be a valid base64.'


def test_post_should_return_not_found_with_invalid_problem_id(client):
    response = client.post('/api/submissions', json=submission_in_complete)

    assert response.status_code == 404
    assert response.json()['detail'] == 'Not found'


def test_post_should_return_not_found_with_invalid_language_type(client, database_problem):
    submission_in_complete['problem_id'] = literal_eval(database_problem.content.decode())['id']
    submission_in_complete['language_type'] = 'java'
    response = client.post('/api/submissions', json=submission_in_complete)

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Invalid language type'
