"""General page routes."""

import imp
from flask_login import current_user, login_user, login_required, logout_user
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from datetime import datetime
from ast import Pass
# from urllib import request
from flask import Blueprint, flash, redirect, render_template, request, url_for
# from flask_login import current_user, login_user
# from flask import current_app as app

from .form import SignupForm, LoginForm
from .model_account import Account
from .. import db, login_manager

# Blueprint Configuration
# signup_bp = Blueprint(
#     "signup_bp", __name__, template_folder="templates", static_folder="static"
# )


"""Routes for user authentication."""
# from xmlrpc.client import DateTime


# Blueprint Configuration
auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup."""
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = Account.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = Account(
                name=form.name.data, email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            # login_user(user)  # Log in as newly created user

            flash(category='success', message="注册成功,请登录！")
            return redirect(url_for("auth_bp.login"))
        else:
            flash(category='error', message="用户已存在！")
    return render_template(
        "signup.jinja2",
        form=form,
        title="注册",
        team="新中国联邦灭共技术支持小组",
        auth_back='auth_bp.login',
        template="main-template auth-template",
    )


@auth_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for("auth_bp.login"))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    from ..index.index import record_notice, E_IP_TYPE

    if (record_notice(request) == E_IP_TYPE .BLACK):
        return redirect("https://www.google.com/")

    # # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("dashboard_bp.dashboard"))

    form = LoginForm()
    # # Validate login attempt
    if form.validate_on_submit():
        user = Account.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            user.last_login = datetime.now()
            db.session.add(user)
            db.session.commit()

            login_user(user)
            next_page = request.args.get("next")

            session["select_01"] = "😁"
            session["select_02"] = "😁😁"
            session["select_03"] = "😁😁😁"
            session["select_04"] = "😁😁😁😁"
            session["select_05"] = "😁😁😁😁😁"
            session["select_06"] = "😁😁😁😁😁😁"

            return redirect(next_page or url_for("dashboard_bp.dashboard"))
        flash(category='error', message="UserNameOrPasswordIncorrect")
        return redirect(url_for("auth_bp.login"))
    return render_template(
        "login.jinja2",
        auth_back='index_bp.index',
        signup='auth_bp.signup',
        form=form,
        title="Login",
        team="新中国联邦灭共技术支持小组",
        template="main-template auth-template",
    )


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return Account.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    # flash("You must be logged in to view that page.")
    return redirect(url_for("auth_bp.login"))
