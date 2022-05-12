
import logging
import os

import pytest
from app import create_app, User
from app.db import db


@pytest.fixture()
def application():
    os.environ['FLASK_ENV'] = 'testing'
    application = create_app()

    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()

