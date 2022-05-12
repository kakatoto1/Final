
def test_request_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Index" in response.data
