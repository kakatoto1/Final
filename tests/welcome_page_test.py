

def test_request_page1(client):
    response = client.get("/welcome")
    assert response.status_code == 200
    assert b"welcome" in response.data
