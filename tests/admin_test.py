"""This test the admin page"""

from app.db.models import User


def test_admin_page(client):
    """This makes a request to the admin page"""

    client.post("/register",
                data=dict(username="test@gmail.com", password="test",
                          about="This is just a test for about me!!!"))

    client.post("/login", data=dict(username="test@gmail.com", password="test"))

    response = client.get("/admin")
    assert response.status_code == 200




def test_admin_can_delete(client):
    """This makes a request to delete a user"""
    for i in range(1, 3):
        response = client.post("/register",
                               data=dict(username=f"test{i}@gmail.com", password="test",
                                         about="This is just a test for about me!!!"))
        # Create a newly registered user
        assert response.status_code == 302

    # Newly registered user is able to log in
    client.post("/login", data=dict(username="test1@gmail.com", password="test"))
    # Log into the admin page
    response = client.get("/admin")
    assert response.status_code == 200

    users = User.query.all()
    assert len(users) == 2

    response = client.post("/users/delete",
                           data=dict(username="test2@gmail.com"))
    assert response.status_code == 302

    users = User.query.all()
    assert len(users) == 1


def test_admin_cannot_delete_itself(client):
    """This makes a request to ensure an admin user cannot be deleted"""

    response = client.post("/register",
                           data=dict(username="test1@gmail.com", password="test",
                                     about="This is just a test for about me!!!"))
    # Create a newly registered user
    assert response.status_code == 302

    # Newly registered user is able to log in
    client.post("/login", data=dict(username="test1@gmail.com", password="test"))
    # Log into the admin page
    response = client.get("/admin")
    assert response.status_code == 200

    users = User.query.all()
    assert len(users)

    response = client.post("/users/delete",
                           data=dict(username="test1@gmail.com"))
    assert response.status_code == 400
