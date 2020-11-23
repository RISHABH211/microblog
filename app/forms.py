from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address")


class LoginForm(
    FlaskForm
):  # LoginForm taken from flask_wtf has its own template formatting
    username1 = StringField(
        "username", validators=[DataRequired()]
    )  # field should have relevant entries
    password1 = PasswordField(
        "password", validators=[DataRequired()]
    )  # field should have relevant entries
    remember_me1 = BooleanField("remember_me")
    submit1 = SubmitField("Sign In")
