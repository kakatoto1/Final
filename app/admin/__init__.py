from flask import Blueprint, render_template
from flask_login import login_required

from app.auth.decorators import admin_required
from app.db.models import User
from app.forms import DeleteForm

admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route("/admin", methods=["GET", "POST"])
@login_required
@admin_required
def index():
    delete_form = DeleteForm()

    pagination = User.query.order_by(User.id).paginate(1, 5, error_out=False)

    return render_template("admin.html", delete_form=delete_form, results=generate_users(pagination),
                           pages=pagination.pages + 1, current_page=1,
                           previous=pagination.prev_num,
                           next=pagination.next_num,
                           has_prev=pagination.has_prev,
                           has_next=pagination.has_next)


@admin.route("/admin/<int:page>", methods=["GET"], defaults={"page": 1})
@login_required
@admin_required
def get_paginated_users(page):
    delete_form = DeleteForm()

    pagination = User.query.order_by(User.id).paginate(page, 5, error_out=False)

    return render_template("admin.html", delete_form=delete_form,
                           results=generate_users(pagination),
                           pages=pagination.pages + 1, current_page=1,
                           previous=pagination.prev_num,
                           next=pagination.next_num,
                           has_prev=pagination.has_prev,
                           has_next=pagination.has_next)


def generate_users(pagination):
    return [{
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "about": user.about,
    } for user in pagination.items]
