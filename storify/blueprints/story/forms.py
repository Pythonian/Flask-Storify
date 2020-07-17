from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, TextAreaField, SubmitField,
                     BooleanField, SelectField)
from wtforms.validators import DataRequired
from storify.blueprints.topic.models import Topic
from .models import Story


class StoryForm(FlaskForm):
    title = StringField('Title', [DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    # enable_comments = BooleanField('Allow Response', default=True)
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    status = SelectField('Status', [DataRequired()],
                         choices=(Story.STATUS))
    topic = SelectField('Topic', coerce=int)
    tags = TagField(
        'Tags',
        description='Separate multiple tags with commas.')
    submit = SubmitField('Publish')

    def save_entry(self, entry):
        self.populate_obj(entry)
        entry.generate_slug()
        return entry

class CommentForm(FlaskForm):
    body = TextAreaField('Comment',
                         validators=[DataRequired(), Length(min=10, max=3000)])
    story_id = HiddenField(validators=[DataRequired()])

    # def validate(self):
    #     if not super().validate():
    #         return False

    #     # Ensure that entry_id maps to a public Entry.
    #     entry = Entry.query.filter(
    #         (Entry.status == Entry.STATUS_PUBLIC) &
    #         (Entry.id == self.entry_id.data)).first()

    #     if not entry:
    #         return False
    #     return True
