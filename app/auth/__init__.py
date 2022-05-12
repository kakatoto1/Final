import logging
import os
from datetime import datetime

from flask import url_for, redirect, Blueprint, render_template, current_app, request
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.utils import secure_filename

from app.db import db
from app.db.models import User, Transaction
from app.forms import RegisterForm, LoginForm, UploadForm
from app.helpers import read_csv

auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route("/", methods=["GET"])
def index():
    users = User.query.all()
    login_form = LoginForm()
    return render_template("login.html", form=login_form, users=users)


@auth.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and user.check_password(login_form.password.data):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("auth.dashboard"))
        return render_template("404.html", username=login_form.username.data)

    return render_template("login.html", form=login_form)


@auth.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    logger = logging.getLogger("myApp")

    page = request.args.get("page", 1, type=int)

    upload_form = UploadForm()

    if current_user.is_authenticated():
        user = User.query.filter_by(id=current_user.id).first()
        if upload_form.validate_on_submit():
            filename = secure_filename(upload_form.file.data.filename)
            filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            upload_form.file.data.save(filepath)
            transactions = read_csv(filepath)

            total = user.total
            for i, transaction in enumerate(transactions):
                transaction = Transaction(amount=transaction["amount"],
                                          transaction_type=transaction["transaction_type"])
                float_amount = float(transaction.amount)

                if float_amount >= 0:
                    total += float_amount
                else:
                    total -= abs(float_amount)

                transaction.user = current_user
                db.session.add(transaction)
                logger.info(f"Adding in Transaction {i+1} at {datetime.utcnow()} for user {user.username}")

            user.total = total
            db.session.add(user)
            db.session.commit()

        user = User.query.filter_by(id=current_user.id).first()
        pagination = Transaction.query.filter_by(user_id=user.id).paginate(page, per_page=10)
        transactions = pagination.items

        return render_template("dashboard.html", username=user.username, transactions=transactions,
                               form=upload_form, total=user.total, pagination=pagination)


@auth.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        new_user = User(username=register_form.username.data,
                        password=register_form.password.data,
                        about=register_form.about.data)
        db.session.add(new_user)
        db.session.commit()
        if new_user.id == 1:
            new_user.is_admin = True
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth.login"), 302)

    return render_template("register.html", form=register_form)


@auth.route("/logout")
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for("auth.login"))
