import os

from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

from app import config

db = SQLAlchemy()

database = Blueprint("database", __name__,)


@database.cli.command("create")
def init_db():
    db.create_all()


@database.before_app_first_request
def create_db_file_if_does_not_exist():
    root = config.Config.BASE_DIR
    # set the name of the apps log folder to logs
    db_dir = os.path.join(root, "..", config.Config.DB_DIR)
    # make a directory if it doesn't exist
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    db.create_all()


@database.before_app_first_request
def create_upload_folder():
    root = config.Config.BASE_DIR
    # set the name of the apps log folder to logs
    upload_folder = os.path.join(root, "..", config.Config.UPLOAD_FOLDER)
    # make a directory if it doesn't exist
    if not os.path.exists(upload_folder):
        os.mkdir(upload_folder)
    db.create_all()
