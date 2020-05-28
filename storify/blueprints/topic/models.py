from datetime import datetime
from storify.blueprints.account.models import User
from storify.blueprints.story.models import Story
from ...extensions import db


likes = db.Table('likes',
                 db.Column('user_id', db.Integer, db.ForeignKey(
                     'users.id'), primary_key=True),
                 db.Column('topic_id', db.Integer, db.ForeignKey(
                     'topics.id'), primary_key=True))


class Topic(db.Model):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    slug = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(100))
    image_file = db.Column(db.String(100))
    # likes = db.Column(db.Integer, default=0)
    # user_likes = db.relationship(User, secondary=likes,
    #                              lazy='subquery',
    #                              backref=db.backref(
    #                                  'topics_liked', lazy='dynamic'))

    def __repr__(self):
        return self.title

    # def get_published_stories(self):
    #     return self.stories.filter(status='published').filter(
    #         Story.published <= datetime.now(pytz.utc))
