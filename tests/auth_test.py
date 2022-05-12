"""This test the auth page"""
import os

import pytest
from flask_login import current_user
from werkzeug.datastructures import FileStorage

from app.db.models import User


def test_home_page(client):
    """This makes a request to the home page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'class="btn btn-primary form-control btn-block"' in response.data
    assert b'type="submit"' in response.data
    assert b'href="/register"' in response.data


def test_invalid_route(client):
    """This makes a request to an invalid route"""
    response = client.get("/random-route")
    assert response.status_code == 404


def test_dashboard_page(client):
    """This makes a request to the dashboard page"""

    users = User.query.all()
    response = client.get("/dashboard")
    # Assert that the following request is redirected
    assert response.status_code == 302
    # No users are currently in the database (i.e. no user to log in with)
    assert len(users) == 0


def test_user_registration(client):
    """This makes a request to register a user"""

    response = client.post("/register",
                           data=dict(username="test@gmail.com", password="test",
                                     about="This is just a test for about me!!!"))
    assert response.status_code == 302
    users = User.query.all()
    # No users are currently in the database (i.e. no user to log in with)
    assert len(users) == 1
    user = User.query.filter_by(username="test@gmail.com").first()
    assert user.id == 1
    # Since the user id is 1, is_admin should be true
    assert user.is_admin is True
    # User has not logged in yet
    assert user.authenticated is False
    assert user.about == "This is just a test for about me!!!"
    assert user.check_password("test")


def test_user_can_access_dashboard(client):
    """This makes a request to register a user"""

    # Create a newly registered user
    response = client.post("/register",
                           data=dict(username="test@gmail.com", password="test",
                                     about="This is just a test for about me!!!"))
    assert response.status_code == 302

    # Newly registered user is able to log in
    response = client.post("/login", data=dict(username="test@gmail.com", password="test"))
    assert response.status_code == 302
    assert current_user is not None


def test_file_upload(client):
    """This makes a request to upload a file and properly stores within user and transaction table"""

    client.post("/register",
                data=dict(username="test@gmail.com", password="test",
                          about="This is just a test for about me!!!"))
    # Newly registered user is able to log in
    client.post("/login", data=dict(username="test@gmail.com", password="test"))

    # New user can access the dashboard
    response = client.get("/dashboard")
    assert response.status_code == 200

    root = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(root, "data/testOne.csv")

    with open(csv_path, "rb") as csv_file:
        my_file = FileStorage(
            stream=csv_file,
            filename="testOne.csv",
            content_type="text/csv"
        )

        response = client.post("/dashboard",
                               data={"file": my_file},
                               content_type="multipart/form-data")
        assert response.status_code == 200

        assert len(User.query.all())

        user = User.query.filter_by(username="test@gmail.com").first()
        assert user
        assert len(user.transactions)


def test_dashboard_is_denied(client):
    """This makes a request to see if a user is denied access when not logged in"""

    client.post("/register",
                data=dict(username="test@gmail.com", password="test",
                          about="This is just a test for about me!!!"))

    response = client.post("/dashboard")
    assert response.status_code == 302

    assert len(User.query.all())

    user = User.query.filter_by(username="test@gmail.com").first()

    assert user.authenticated is False


def test_csv_file_cannot_be_uploaded(client):
    """This makes a request to see if a user cannot upload a csv file when not logged in"""

    client.post("/register",
                data=dict(username="test@gmail.com", password="test",
                          about="This is just a test for about me!!!"))

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/testOne.csv")

    with open(path, "rb") as csv_file:
        my_file = FileStorage(
            stream=csv_file,
            filename="test.csv",
            content_type="text/csv"
        )

        client.post("/dashboard",
                    data={"file": my_file},
                    content_type="multipart/form-data")

        user = User.query.filter_by(username="test@gmail.com").first()
        assert user
        assert len(user.transactions) == 0


def test_empty_file_upload(client):
    """This makes a request to upload a transaction file that is empty"""

    client.post("/register",
                data=dict(username="test@gmail.com", password="test",
                          about="This is just a test for about me!!!"))
    # Newly registered user is able to log in
    client.post("/login", data=dict(username="test@gmail.com", password="test"))

    # New user can access the dashboard
    response = client.get("/dashboard")
    assert response.status_code == 200

    root = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(root, "data/empty.csv")

    with open(csv_path, "rb") as csv_file:
        my_file = FileStorage(
            stream=csv_file,
            filename="empty.csv",
            content_type="text/csv"
        )

        response = client.post("/dashboard",
                               data={"file": my_file},
                               content_type="multipart/form-data")
        assert response.status_code == 200

        assert len(User.query.all())

        user = User.query.filter_by(username="test@gmail.com").first()
        assert user
        assert len(user.transactions) == 0


def test_corrupt_file_upload(client):
    """This makes a request to upload a transaction
    file that is corrupted (i.e. bad inputs)"""

    client.post("/register",
                data=dict(username="test@gmail.com", password="test",
                          about="This is just a test for about me!!!"))
    # Newly registered user is able to log in
    client.post("/login", data=dict(username="test@gmail.com", password="test"))

    # New user can access the dashboard
    response = client.get("/dashboard")
    assert response.status_code == 200

    root = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(root, "data/corrupt_data.csv")

    with open(csv_path, "rb") as csv_file:
        my_file = FileStorage(
            stream=csv_file,
            filename="corrupt_data.csv",
            content_type="text/csv"
        )

        with pytest.raises(Exception):
            client.post("/dashboard",
                        data={"file": my_file},
                        content_type="multipart/form-data")

        assert len(User.query.all())

        user = User.query.filter_by(username="test@gmail.com").first()
        assert user
        assert len(user.transactions) == 0