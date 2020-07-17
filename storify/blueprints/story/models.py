from collections import OrderedDict
from datetime import datetime
from storify.blueprints.account.models import User
from storify.blueprints.tag.models import Tag
from ...extensions import db


tag_x_story = db.Table('tag_x_story',
                       db.Column('tag_id', db.Integer, db.ForeignKey(
                           'tags.id'), primary_key=True),
                       db.Column('story_id', db.Integer, db.ForeignKey(
                           'stories.id'), primary_key=True))

favorites = db.Table('favorites',
                     db.Column('user_id', db.Integer, db.ForeignKey(
                         'users.id'), primary_key=True),
                     db.Column('story_id', db.Integer, db.ForeignKey(
                         'stories.id'), primary_key=True))

bookmarks = db.Table('bookmarks',
                     db.Column('user_id', db.Integer, db.ForeignKey(
                         'users.id'), primary_key=True),
                     db.Column('story_id', db.Integer, db.ForeignKey(
                         'stories.id'), primary_key=True))


class Story(db.Model):
    STATUS = OrderedDict([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('deleted', 'Deleted'),
    ])

    __tablename__ = 'stories'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), index=True)
    slug = db.Column(db.String(100), unique=True)
    image = db.Column(db.String(36))
    excerpts = db.Column(db.String(40))
    body = db.Column(db.Text)
    status = db.Column(db.Enum(*STATUS, name='status_types',
                               native_enum=False), index=True, nullable=False,
                       server_default='published')
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    enable_comments = db.Column(db.Boolean, default=True)
    comments = db.relationship('Comment', backref='entry', lazy='dynamic')
    created = db.Column(db.DateTime, onupdate=datetime.utcnow)
    published = db.Column(db.DateTime)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    topic = db.Column(db.Integer,
                      db.ForeignKey('topics.id',
                                    cascade='all, delete-orphan'))
    read_time = db.Column(db.Integer, default=0)
    impressions = db.Column(db.Integer, default=0)
    author = db.relationship(User,
                             backref=db.backref('stories', lazy='dynamic'))
    tags = db.relationship(Tag, secondary=tag_x_story, lazy='subquery',
                            backref=db.backref('stories', lazy='dynamic'))
    featured = db.Column(db.Boolean, default=False)
    favorites = db.Column(db.Integer, default=0)
    # user_favorites = db.relationship(User, secondary=favorites,
    #                                  lazy='subquery',
    #                                  backref=db.backref(
    #                                      'stories_favorited', lazy='dynamic'))
    bookmarks = db.Column(db.Integer, default=0)
    # user_bookmarks = db.relationship(User, secondary=bookmarks,
    #                                  lazy='subquery',
    #                                  backref=db.backref(
    #                                      'stories_bookmarked', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f'Story: {self.title}'

    def get_excerpts(self):
        if len(self.body) > 140:
            return '{0}...'.format(self.body[:140])
        else:
            return self.body

    @staticmethod
    def latest():
        return Story.query.order_by((Story.updated.desc())).limit(3)


class Comment(db.Model):
    STATUS_PENDING_MODERATION = 0
    STATUS_PUBLIC = 1
    STATUS_SPAM = 8
    STATUS_DELETED = 9

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    writer = db.Column(db.String(80))
    created = db.Column(
        db.DateTime(timezone=True),
        default=datetime.now)
    last_modified = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    ip_address = db.Column(db.String(64))
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)

    def __repr__(self):
        return f'<Comment from {self.writer}>'
