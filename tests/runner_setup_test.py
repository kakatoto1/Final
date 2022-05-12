
import logging
import os

import pytest
from app import create_app, User
from app.db import db

@pytest.fixture()
def runner(application):
    return application.test_cli_runner()
