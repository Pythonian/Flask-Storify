from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)
# from flask_wtf.file import FileAllowed, FileField

from storify.blueprints.account.models import User


class EditProfileForm(FlaskForm):
    # username = StringField('Username',
    #                        validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First name', validators=[Length(min=0, max=60)])
    last_name = StringField('Last name', validators=[Length(min=0, max=60)])
    about = TextAreaField('About me', validators=[Length(min=0, max=140)])
    # picture = FileField('Update Profile Picture', validators=[
    #                     FileAllowed(['jpg', 'png'])])
    date = DateField('Date')
    submit = SubmitField('Save Changes')

    # def validate_username(self, username):
    #     if username.data != current_user.username:
    #         user = User.query.filter_by(username=username.data).first()
    #         if user:
    #             raise ValidationError(
    #                 'That username is taken. Please choose a different one.')


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

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data.lower()).first():
                raise ValidationError('Email already registered.')
