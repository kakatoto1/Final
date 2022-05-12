from flask import Blueprint, render_template, abort, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from app import db
from app.auth.decorators import admin_required
from app.db.models import User
from app.forms import EditForm, DeleteForm

users = Blueprint("users", __name__, template_folder="templates")


@users.route("/users/edit", methods=["GET", "POST"])
@login_required
def edit():
    edit_form = EditForm()

    user = User.query.filter_by(username=current_user.username).first()

    if user:
        if edit_form.validate_on_submit():
            user.username = edit_form.username.data
            user.password = generate_password_hash(edit_form.password.data)
            user.about = edit_form.about.data
            db.session.add(user)
            db.session.commit()

        edit_form.about.data = user.about

        return render_template("edit.html", result={
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "about": user.about,
        }, edit_form=edit_form)

    return render_template("404.html")


@users.route("/users/delete", methods=["POST"])
@login_required
@admin_required
def delete():
    delete_form = DeleteForm()

    if delete_form.validate_on_submit():
        user = User.query.filter_by(username=delete_form.username.data).first()
        if user and not user.is_admin:
            db.session.delete(user)
            db.session.commit()
        else:
            abort(400, "An Admin cannot be deleted!")

    return redirect(url_for("admin.index"))
