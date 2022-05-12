
import logging
import os

import app.config


def test_production_config(application):
    application.config.from_object('app.config.ProductionConfig')
    assert not application.config['DEBUG']
    assert not application.config['TESTING']
