
import httpx
import pytest
import base64

MASTER_API_KEY = "57fba00c-aa3d-4009-87d6-700f58a4032b"
BASE_URL = "http://127.0.0.1:8000"

HEADERS = {
    "Authorization": f"Bearer {MASTER_API_KEY}"
}

async def create_problem_for_submission(client):
    problem_data = {
        "name": "Submission Test Problem",
        "description": "A problem for testing submissions",
        "entry_description": "Input is a string",
        "output_description": "Output is the same string"
    }
    response = await client.post(f"{BASE_URL}/v0/problems", json=problem_data, headers=HEADERS)
    return response.json()["id"]

@pytest.mark.asyncio
async def test_create_submission():
    async with httpx.AsyncClient() as client:
        problem_id = await create_problem_for_submission(client)
        code = "print(\"hello world\")"
        encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')

        submission_data = {
            "problem_id": problem_id,
            "language_type": "py",
            "content": encoded_code
        }
        response = await client.post(f"{BASE_URL}/v0/submissions", json=submission_data, headers=HEADERS)
        assert response.status_code == 201
        assert response.json()["problem_id"] == problem_id

@pytest.mark.asyncio
async def test_create_submission_problem_not_found():
    async with httpx.AsyncClient() as client:
        code = "print(\"hello world\")"
        encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')

        submission_data = {
            "problem_id": "00000000-0000-0000-0000-000000000000",
            "language_type": "py",
            "content": encoded_code
        }
        response = await client.post(f"{BASE_URL}/v0/submissions", json=submission_data, headers=HEADERS)
        assert response.status_code == 409

@pytest.mark.asyncio
async def test_get_submission():
    async with httpx.AsyncClient() as client:
        problem_id = await create_problem_for_submission(client)
        code = "print(\"hello world\")"
        encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')

        submission_data = {
            "problem_id": problem_id,
            "language_type": "py",
            "content": encoded_code
        }
        create_response = await client.post(f"{BASE_URL}/v0/submissions", json=submission_data, headers=HEADERS)
        submission_id = create_response.json()["id"]

        get_response = await client.get(f"{BASE_URL}/v0/submissions/{submission_id}", headers=HEADERS)
        assert get_response.status_code == 200
        assert get_response.json()["id"] == submission_id

@pytest.mark.asyncio
async def test_query_submissions():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/v0/submissions", headers=HEADERS)
        assert response.status_code == 200
        assert isinstance(response.json()["results"], list)
