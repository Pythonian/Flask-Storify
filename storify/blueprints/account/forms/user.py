from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

from storify.blueprints.account.models import User


class EditProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[Length(min=0, max=60)])
    last_name = StringField('Last name', validators=[Length(min=0, max=60)])
    about = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Save Changes')


class PasswordChangeForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.'),
        Length(min=4)])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField('Update Password')


class ChangeEmailForm(FlaskForm):
    email = EmailField('New Email', validators=[DataRequired(),
                                                Length(min=1, max=60),
                                                Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')
