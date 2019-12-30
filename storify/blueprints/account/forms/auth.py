from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Regexp,
                                ValidationError)

from storify.blueprints.account.models import User


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(),
                                            Length(min=1, max=60),
                                            Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(min=4, max=20),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.'),
        Length(min=4)])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PasswordResetRequestForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(1, 60),
                                            Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), Length(min=4), EqualTo('password2',
                                               message='Passwords must match')])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField('Reset Password')
