"""This tests pagination"""
import os

from werkzeug.datastructures import FileStorage
from app.db.models import User, Transaction


def test_transaction_pagination(client):
    """This makes a request to test pagination"""

    client.post("/register",
                data=dict(username="test2@gmail.com", password="test",
                          about="This is just a test for about me!!!"))
    # Newly registered user is able to log in
    client.post("/login", data=dict(username="test2@gmail.com", password="test"))

    root = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(root, "data/testOne.csv")

    with open(csv_path, "rb") as csv_file:
        my_file = FileStorage(
            stream=csv_file,
            filename="testOne.csv",
            content_type="text/csv"
        )

        client.post("/dashboard",
                    data={"file": my_file},
                    content_type="multipart/form-data")

        assert len(User.query.all())

        user = User.query.filter_by(username="test2@gmail.com").first()
        assert user
        assert len(user.transactions)

    pagination = Transaction.query.filter_by(user_id=user.id).paginate(1, 5)
    assert len(pagination.items) == 5
    assert pagination.has_next is True


def test_admin_pagination(client):
    """This makes a request to admin pagination"""
    for i in range(1, 11):
        response = client.post("/register",
                               data=dict(username=f"test{i}@gmail.com", password="test",
                                         about="This is just a test for about me!!!"))
        # Create a newly registered user
        assert response.status_code == 302

    pagination = User.query.paginate(1, 5)
    assert len(pagination.items) == 5
    assert pagination.has_next is True

    pagination = User.query.paginate(2, 5)
    assert len(pagination.items) == 5
    assert pagination.has_next is False

    pagination = User.query.paginate(3, 5, error_out=False)
    assert len(pagination.items) == 0
