
def test_request_page_not_found(client):
    response = client.get("/page5")
    assert response.status_code == 404