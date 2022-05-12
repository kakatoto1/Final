
import logging
import os

import pytest
from app import create_app, User
from app.db import db


@pytest.fixture()
def add_user(application):
    with application.app_context():
        #new record
        user = User('keith@webizly.com', 'testtest')
        db.session.add(user)
        db.session.commit()
