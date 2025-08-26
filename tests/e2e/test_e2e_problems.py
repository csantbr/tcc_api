
import httpx
import pytest

MASTER_API_KEY = "57fba00c-aa3d-4009-87d6-700f58a4032b"
BASE_URL = "http://127.0.0.1:8000"

HEADERS = {
    "Authorization": f"Bearer {MASTER_API_KEY}"
}

@pytest.mark.asyncio
async def test_create_problem():
    async with httpx.AsyncClient() as client:
        problem_data = {
            "name": "Test Problem E2E",
            "description": "Test Description E2E",
            "entry_description": "Test Entry Description E2E",
            "output_description": "Test Output Description E2E"
        }
        response = await client.post(f"{BASE_URL}/v0/problems", json=problem_data, headers=HEADERS)
        assert response.status_code == 201
        assert response.json()["name"] == "Test Problem E2E"

@pytest.mark.asyncio
async def test_get_problem():
    async with httpx.AsyncClient() as client:
        problem_data = {
            "name": "Test Problem E2E Get",
            "description": "Test Description E2E Get",
            "entry_description": "Test Entry Description E2E Get",
            "output_description": "Test Output Description E2E Get"
        }
        create_response = await client.post(f"{BASE_URL}/v0/problems", json=problem_data, headers=HEADERS)
        problem_id = create_response.json()["id"]

        get_response = await client.get(f"{BASE_URL}/v0/problems/{problem_id}", headers=HEADERS)
        assert get_response.status_code == 200
        assert get_response.json()["id"] == problem_id

@pytest.mark.asyncio
async def test_get_problem_not_found():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/v0/problems/00000000-0000-0000-0000-000000000000", headers=HEADERS)
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_problem():
    async with httpx.AsyncClient() as client:
        problem_data = {
            "name": "Test Problem E2E Update",
            "description": "Test Description E2E Update",
            "entry_description": "Test Entry Description E2E Update",
            "output_description": "Test Output Description E2E Update"
        }
        create_response = await client.post(f"{BASE_URL}/v0/problems", json=problem_data, headers=HEADERS)
        problem_id = create_response.json()["id"]

        update_data = {"name": "Updated Problem Name"}
        update_response = await client.put(f"{BASE_URL}/v0/problems/{problem_id}", json=update_data, headers=HEADERS)
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated Problem Name"

@pytest.mark.asyncio
async def test_query_problems():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/v0/problems", headers=HEADERS)
        assert response.status_code == 200
        assert isinstance(response.json()["results"], list)
