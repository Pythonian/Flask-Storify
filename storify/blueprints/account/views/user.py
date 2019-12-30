from storify.blueprints.account.forms.user import (
    PasswordChangeForm, ChangeEmailForm, EditProfileForm)
from storify.blueprints.account.models import User
from flask_login import current_user, login_required
from storify.extensions import db
from storify.utils.email import send_email
from flask import Blueprint, flash, redirect, render_template, url_for, abort

user = Blueprint('user', __name__,
                 template_folder='../templates', url_prefix='/user/')


@user.route('/<username>/', methods=['GET'])
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.confirmed is False:
        abort(404)
    return render_template('user/profile.html', user=user)


@user.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.about = form.about.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('user.profile', username=current_user.username))
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.about.data = current_user.about
    return render_template('user/settings.html', form=form)


@user.route('/settings/password/', methods=['GET', 'POST'])
@login_required
def password_change():
    """Change an existing user's password."""
    form = PasswordChangeForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            send_email(current_user.email, 'Password Change Notification',
                       'user/email/password_change',
                       user=current_user._get_current_object())
            flash('Your password has been updated.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Original password is invalid. Try again.', 'danger')
    return render_template('user/password_change.html', form=form)


@user.route('/settings/change-email/', methods=['GET', 'POST'])
@login_required
def change_email_request():
    """Respond to existing user's request to change their email."""
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'user/email/change_email',
                       user=current_user._get_current_object(), token=token)
            flash(f'A confirmation link has been sent to {new_email}.',
                  'info')
            return redirect(url_for('user.change_email_request'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('user/change_email.html', form=form)


@user.route('/settings/change-email/<token>/', methods=['GET', 'POST'])
@login_required
def change_email(token):
    """Change existing user's email with provided token."""
    if current_user.confirm_email_change_token(token):
        db.session.commit()
        flash('Your email address has been updated.', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('user.profile'))


@user.route('/<username>/follow/')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        flash('You cannot follow yourself!', 'warning')
        return redirect(url_for('user.profile', username=username))
    if current_user.is_following(user):
        flash(f'You are already following {username}.', 'info')
        return redirect(url_for('user.profile', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f'You are now following {username}.', 'success')
    return redirect(url_for('user.profile', username=username))


@user.route('/<username>/unfollow/')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        flash('You cannot unfollow yourself!', 'warning')
        return redirect(url_for('user.profile', username=username))
    if not current_user.is_following(user):
        flash(f'You are not following {username}.', 'info')
        return redirect(url_for('user.profile', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You have stopped following {username}.', 'success')
    return redirect(url_for('user.profile', username=username))


@user.route('/<username>/followers/')
def followers(username):
    user = User.query.filter_by(username=username).first_or_404()
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in user.followers.all()]
    return render_template('user/follows.html', user=user, followers=True,
                           title="People followed by ", follows=follows)


@user.route('/<username>/following/')
def following(username):
    user = User.query.filter_by(username=username).first_or_404()
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in user.followed.all()]
    return render_template('user/follows.html', user=user,
                           title="People following ", follows=follows)
