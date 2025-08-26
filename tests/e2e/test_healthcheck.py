
import httpx

def test_healthcheck():
    response = httpx.get("http://127.0.0.1:8000/v0/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
