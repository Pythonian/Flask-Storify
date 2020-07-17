from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash

from ...extensions import db


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    """ User table instance. """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(20), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    about = db.Column(db.String(140))
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    avatar = db.Column(db.String(200))

    confirmed = db.Column(db.Boolean, default=False)
    verified_account = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    stories = db.relationship('Story', backref='author', lazy='dynamic')

    def __repr__(self):
        """ Return string representation of User instance. """
        return f'<User {self.username}>'

    def ping(self):
        """ Update the last visit of a User. """
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
        """ Prevent password from being accessed. """
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password.

        :param password: The password to be hashed
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password.

        :param password: The plaintext password to compare against the hash
        """
        return check_password_hash(self.password_hash, password)

    def generate_email_confirmation_token(self, expiration=3600):
        """
        Generate a confirmation token to email to a new user.

        :param expiration: Number in seconds the token will expire after
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm_email_token(self, token):
        """
        Verify that the provided token is for the actual user id.

        :param token:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except (BadSignature, SignatureExpired):
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_password_reset_token(self, expiration=3600):
        """
        Generate a password reset change token to email to an existing user.

        :param expiration: Number in seconds the token will expire after
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def confirm_password_token(token, new_password):
        """
        Verify the new password for the user.

        :param token:
        :param new_password:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except (BadSignature, SignatureExpired):
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        """
        Generate an email change token to email an existing user.

        :param new_email:
        :param expiration:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id,
                        'new_email': new_email}).decode('utf-8')

    def confirm_email_change_token(self, token):
        """
        Verify the new email is for the actual user.

        :param token:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except (BadSignature, SignatureExpired):
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    @property
    def get_screen_name(self):
        """ Return the username if the first and last name isn't provided."""
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.username}'

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    # def notify_commented(self, story):
    #     if self.user != story.author:
    #         Notification(notification_type=Notification.COMMENTED,
    #             from_user=self.user,
    #             to_user=story.author,
    #             story=story).save()

    # def notify_also_commented(self, story):
    #     comments = story.get_comments()
    #     users = []
    #     for comment in comments:
    #         if comment.name != self.user and comment.name != story.author:
    #             users.append(comment.name.pk)
    #     users = list(set(users))
    #     for user in users:
    #         Notification(notification_type=Notification.ALSO_COMMENTED,
    #             from_user=self.user,
    #             to_user=User(id=user),
    #             story=story).save()

    # def notify_followed(self, follow):
    #     if self.user != follow.to_user:
    #         Notification(notification_type=Notification.FOLLOWED,
    #             from_user=self.user,
    #             to_user=follow.to_user,
    #             follow=follow).save()

    # def notify_favorited(self, story):
    #     if self.user != story.author:
    #         Notification(notification_type=Notification.FAVORITED,
    #             from_user=self.user,
    #             to_user=story.author,
    #             story=story).save()

    # def unnotify_favorited(self, story):
    #     if self.user != story.author:
    #         Notification.objects.filter(
    #             notification_type=Notification.FAVORITED,
    #             from_user=self.user,
    #             to_user=story.author,
    #             story=story).delete()
