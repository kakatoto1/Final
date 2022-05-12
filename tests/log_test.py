"""This tests that when transactions are made it's properly logged"""

import os

from werkzeug.datastructures import FileStorage

from app.db.models import User


def test_transactions_are_logged_for_a_user(client):
    """This tests that when we insert transactions
    for a user with a non-empty file, it's logged"""
    root = os.path.dirname(os.path.abspath(__file__))
    app_logs = os.path.join(root, "../logs/myapp.log")
    os.remove(app_logs)
    assert os.path.isfile(app_logs) is False
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
    assert os.path.isfile(app_logs) is True

    with open(app_logs, "rb") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        assert len(lines)


def test_transactions_are_not_logged_for_an_empty_file(client):
    """This tests that when we insert tractions
    for a user with an empty file, nothing is logged"""
    root = os.path.dirname(os.path.abspath(__file__))
    app_logs = os.path.join(root, "../logs/myapp.log")
    os.remove(app_logs)
    assert os.path.isfile(app_logs) is False
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
    assert os.path.isfile(app_logs) is True

    with open(app_logs, "rb") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        assert len(lines) == 0
