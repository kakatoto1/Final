

def test_request_about(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data
