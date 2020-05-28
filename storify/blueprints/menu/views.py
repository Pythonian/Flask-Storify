from flask import Blueprint, render_template
from storify.blueprints.story.models import Story
from storify.blueprints.topic.models import Topic

menu = Blueprint('menu', __name__, template_folder='templates')


@menu.route('/')
def home():
    latest_stories = Story.published.desc()
    return render_template('menu/home.html',
                           latest_stories=latest_stories)


@menu.route('/topics/')
def topics():
    topics = Topic.query.all()
    return render_template('menu/topics.html', topics=topics)


@menu.route('/popular/')
def popular():
    return render_template('menu/popular.html')


@menu.route('/people/')
def people():
    return render_template('menu/people.html')
