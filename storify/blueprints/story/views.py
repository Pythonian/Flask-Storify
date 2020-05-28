from datetime import datetime
from flask import (Blueprint, render_template, url_for, redirect, abort, flash)
from flask_login import login_required, current_user
from storify.extensions import db
from storify.blueprints.topic.models import Topic
from .forms import StoryForm
from .models import Story

story = Blueprint('story', __name__, template_folder='templates')


@story.route('/new-story', methods=['GET', 'POST'])
@login_required
def create():
    form = StoryForm()
    if form.validate_on_submit():
        story = Story(body=form.body.data,
                      title=form.title.data,
                      user_id=current_user.id,
                      published=datetime.utcnow(),
                      topic=Topic.query.get(form.topic.data))
        db.session.add(story)
        db.session.commit()
        return redirect(url_for('story.detail', id=story.id))
    return render_template('story/form.html', form=form)


@story.route('/story/<int:id>')
def detail(id):
    story = Story.query.get_or_404(id)
    return render_template('story/detail.html', story=story)


@story.route('/story/<int:id>/edit/', methods=['GET', 'POST'])
def edit(id):
    story = Story.query.get_or_404(id)
    form = StoryForm(obj=story)
    if story.user_id != current_user.id:
        abort(403)
    if form.validate_on_submit():
        story.title = form.title.data
        story.body = form.body.data
        story.updated = datetime.utcnow()
        db.session.add(story)
        db.session.commit()
        return redirect(url_for('story.detail', id=story.id))
    return render_template('story/form.html', form=form, story=story)


@story.route('/story/<int:id>/delete/', methods=['GET', 'POST'])
def delete(id):
    story = Story.query.get_or_404(id)
    if story.user_id != current_user.id:
        abort(403)
    db.session.delete(story)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('user.stories'))
