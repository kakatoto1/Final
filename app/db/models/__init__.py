from datetime import datetime

from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import db
from flask_login import UserMixin


class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="transactions", uselist=False)

    def __init__(self, amount, transaction_type):
        self.amount = amount
        self.transaction_type = transaction_type


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    about = db.Column(db.String(300), nullable=True, unique=False)
    authenticated = db.Column(db.Boolean, default=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow())
    is_admin = db.Column(db.Boolean(), nullable=False, server_default="0")
    total = db.Column(db.Float, server_default="0.0", nullable=False)
    transactions = db.relationship("Transaction", back_populates="user", cascade="all, delete")

    def __init__(self, username, password, about):
        self.username = username
        self.password = generate_password_hash(password)
        self.about = about

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return self.authenticated
