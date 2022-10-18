def test_get_stores(client):
    response = client.get(f"/api/problems")
    breakpoint()
    assert response.status_code == 200