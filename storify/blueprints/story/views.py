from datetime import datetime
from flask import (Blueprint, render_template, url_for, redirect, abort, flash)
from flask_login import login_required, current_user
from slugify import slugify
from werkzeug import secure_filename
from werkzeug.contrib.atom import AtomFeed
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
        # image_file = request.files['file']
        # filename = secure_filename(image_file.filename)
        # image_file.save(filename)
        db.session.add(story)
        db.session.commit()
        flash(f'Story {story.title} created successfully', 'success')
        return redirect(url_for('story.detail', slug=story.slug))
    return render_template('story/form.html', form=form)

@login_required
@story.route('/story/<slug>/')
def detail(slug):
    story = Story.query.get_or_404(slug=slug)
    form = CommentForm(data={'entry_id': entry.id})
    return render_template('story/detail.html', story=story, form=form)

@login_required
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
        return redirect(url_for('story.detail', slug=story.slug))
    return render_template('story/form.html', form=form, story=story)


@login_required
@story.route('/story/<int:id>/delete/', methods=['GET', 'POST'])
def delete(id):
    story = Story.query.get_or_404(id)
    if story.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        story.status = Story.DELETED
        db.session.add(story)
        db.session.commit()
    # db.session.delete(story)
        flash('Your post has been deleted', 'success')
        return redirect(url_for('user.stories'))
    return render_template('delete.html', story=story)


@app.route('/feeds/')
def recent_feed():
    """
    View used to create Atom feeds to the blog readers
    """
    feed = AtomFeed(
        'Latest Blog Posts',
        feed_url=request.url,
        url=request.url_root,
        author=request.url_root
    )
    entries = Entry.query.filter(Entry.status == Entry.PUBLISHED).\
        order_by(Entry.created.desc()).limit(15).all()

    for entry in entries:
        feed.add(
            entry.title,
            entry.body,
            content_type='html',
            url=urljoin(request.url_root, url_for(
                'post', slug=entry.slug)),
            updated=entry.updated,
            published=entry.created)

    return feed.get_response()
