"""This test user model"""
from app import db
from app.db.models import User, Transaction


def test_cascade_operations(application):
    """This tests a user is added and delete cascade operations"""
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Transaction).count() == 0
        # Add a user
        user = User("test@random.com", "testtest", "This tests that an about section is created")
        db.session.add(user)
        user = User.query.filter_by(username='test@random.com').first()
        # asserting that the user retrieved is correct
        assert user.username == "test@random.com"
        # Add transactions
        user.transactions = [Transaction(500, "CREDIT"),
                             Transaction(-1000, "DEBIT"), Transaction(1000, "CREDIT")]
        db.session.commit()
        # Assert # of transactions is two
        assert db.session.query(Transaction).count() == 3
        transaction = Transaction.query.filter_by(transaction_type="CREDIT").first()
        assert transaction.amount == 500
        # changing the amount of the transaction
        transaction.amount = 1000
        # saving the new amount of the transaction
        db.session.commit()
        transaction = Transaction.query.filter_by(transaction_type="CREDIT").first()
        assert transaction.amount == 1000
        # checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Transaction).count() == 0


def test_edit_page(client):
    """This makes a request to the edit user page"""
    client.post("/register",
                data=dict(username="test@gmail.com", password="test",
                          about="This is just a test for about me!!!"))
    # Newly registered user is able to log in
    response = client.post("/login", data=dict(username="test@gmail.com", password="test"))
    assert response.status_code == 302
    response = client.get("/users/edit")
    assert response.status_code == 200
    assert b'type="submit"' in response.data
    assert b'User Details' in response.data


def test_edit_user(client):
    """This makes a request to edit a user"""
    client.post("/register",
                data=dict(username="test@gmail.com", password="test",
                          about="This is just a test for about me!!!"))
    # Newly registered user is able to log in
    response = client.post("/login", data=dict(username="test@gmail.com", password="test"))
    assert response.status_code == 302

    response = client.get("/users/edit")
    assert response.status_code == 200
    password = "new_password"
    about = "Test to see if I can edit"

    response = client.post("/users/edit",
                           data=dict(username="test@gmail.com", password=password,
                                     about=about))
    assert response.status_code == 200

    user = User.query.filter_by(username="test@gmail.com").first()
    assert user.check_password(password)
    assert user.about == about
