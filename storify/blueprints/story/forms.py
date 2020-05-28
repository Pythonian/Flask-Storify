from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SubmitField,
                     BooleanField, SelectField)
from wtforms.validators import DataRequired
from storify.blueprints.topic.models import Topic
from .models import Story


class StoryForm(FlaskForm):
    title = StringField('Title', [DataRequired()])
    body = TextAreaField([DataRequired()])
    # enable_comments = BooleanField('Allow Response', default=True)
    # image;
    # status = SelectField('Status', [DataRequired()],
    #                      choices=(Story.STATUS))
    topic = SelectField('Topic', coerce=int)
    submit = SubmitField('Publish')


# class CommentForm(FlaskForm):
#     body = TextField()
