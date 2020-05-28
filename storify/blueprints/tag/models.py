import pytz
from datetime import datetime
from storify.blueprints.story.models import Story
from ...extensions import db


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), index=True)
    slug = db.Column(db.String(20))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.title

    @staticmethod
    def get_popular_tags():
        tags = Tag.query.all()
        count = {}
        for tag in tags:
            if tag.story.status == Story.status.published:
                if tag.title in count:
                    count[tag.title] = count[tag.title] + 1
                else:
                    count[tag.title] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]

    def published_stories_tag(self):
        """
        Returns published stories for a tag instance.
        """
        return self.stories.filter(status='published').filter(
            Story.published <= datetime.now(pytz.utc))
