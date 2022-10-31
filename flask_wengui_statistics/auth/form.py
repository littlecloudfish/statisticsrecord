"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class SignupForm(FlaskForm):
    """User Sign-up Form."""
    name = StringField("名字", validators=[DataRequired()], render_kw={
                       'class': 'form-control mt-1 rounded-pill', 'readonly': 'true'})
    email = StringField(
        "邮箱",
        validators=[
            Length(min=6),
            Email(message="Enter a valid email."),
            DataRequired(),
        ], render_kw={'class': 'form-control mt-1 rounded-pill', 'readonly': 'true'}
    )
    password = PasswordField(
        "密码",
        validators=[
            DataRequired(),
            Length(min=6, message="Select a stronger password."),
        ], render_kw={'class': 'form-control mt-1 rounded-pill', 'readonly': 'true'}
    )
    confirm = PasswordField(
        "重复密码",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ], render_kw={'class': 'form-control mt-1 rounded-pill', 'readonly': 'true'}
    )
    # website = StringField("Website", validators=[Optional()])
    submit = SubmitField(
        "注册", render_kw={'class': 'form-control mt-1 rounded-pill', 'readonly': 'true'})


class LoginForm(FlaskForm):
    """User Log-in Form."""

    email = StringField(
        "电子邮箱", validators=[DataRequired(), Email(message="Enter a valid email.")], render_kw={'class': 'form-control mt-1 rounded-pill', 'autofocus': 'true'}
    )
    password = PasswordField("登录密码", validators=[DataRequired()], render_kw={
                             'class': 'form-control mt-1 rounded-pill'})
    submit = SubmitField(
        "登录", render_kw={'class': 'form-control mt-1 rounded-pill'})
