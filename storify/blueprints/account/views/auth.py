from storify.blueprints.account.forms.auth import (
    LoginForm, PasswordResetForm, PasswordResetRequestForm, RegistrationForm)

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.urls import url_parse
from storify.extensions import db
from storify.utils.email import send_email

from storify.blueprints.account.models import User

auth = Blueprint('auth', __name__,
                 template_folder='../templates', url_prefix='/auth/')


@auth.before_app_request
def before_request():
    """Force user to confirm email before accessing login-required routes."""
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

# Track the last page a user visited
# @app.before_request
# def _last_page_visited():
#      if "current_page" in session:
#      session["last_page"] = session["current_page"]
#      session["current_page"] = request.path


@auth.route('/unconfirmed/')
def unconfirmed():
    """Catch users with unconfirmed emails."""
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('home'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next = request.args.get('next')
        if not next or url_parse(next).netloc != '':
            next = url_for('home')
        return redirect(next)
    return render_template('auth/login.html', form=form)


@auth.route('/logout/')
@login_required
def logout():
    """Handle requests to the /logout/ route and logs a user out."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(request.args.get('next') or url_for('home'))


@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    """Register a new user, and send them a confirmation email."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data.lower(),
                    password=form.password.data,
                    favorite_club=form.favorite_club.data)
        db.session.add(user)
        db.session.commit()

        # Require user to confirm email
        token = user.generate_email_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash(
            f'A confirmation email has been sent to {user.email}.', 'warning')

        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)


@auth.route('/confirm-account/<token>/')
@login_required
def confirm(token):
    """Confirm new user's account with provided token."""
    if current_user.confirmed:
        flash('Your account has already been confirmed.', 'info')
        return redirect(url_for('home'))
    if current_user.confirm_email_token(token):
        db.session.commit()
        send_email(current_user.email, 'Account Activation Successful',
                   'auth/email/successful',
                   user=current_user._get_current_object())
        flash('Your account has been confirmed.', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('home'))


@auth.route('/confirm-account/')
@login_required
def resend_confirmation():
    """Resend email confirmation token to a registered user."""
    if current_user.confirmed:
        flash('Your account has already been confirmed.', 'info')
        return redirect(url_for('home'))
    try:
        token = current_user.generate_email_confirmation_token()
        send_email(current_user.email, 'Confirm Your Account',
                   'auth/email/confirm',
                   user=current_user._get_current_object(), token=token)
        flash(
            f'A new confirmation email has been sent to {current_user.email}.',
            'success')
    except IntegrityError:
        flash('Unable to send an email to confirm your email address.',
              'danger')
    return redirect(url_for('auth.login'))


@auth.route('/reset-password/', methods=['GET', 'POST'])
def password_reset_request():
    """Respond to existing user's request to reset their password."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_password_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token)
        flash(
            f'Instructions to reset your password '
            'has been sent to {form.email.data}.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset-password/<token>/', methods=['GET', 'POST'])
def password_reset(token):
    """Reset an existing user's password."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.confirm_password_token(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated. Please log in to continue.',
                  'success')
            return redirect(url_for('auth.login'))
        else:
            flash('The password reset link is an '
                  'invalid or expired token', 'danger')
            return redirect(url_for('home'))
    return render_template('auth/password_reset_confirm.html', form=form)
