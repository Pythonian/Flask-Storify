from flask import render_template, Blueprint
from flask_login import current_user
from .models import Topic

topic = Blueprint('topic', __name__, url_prefix='/topic/')


# @topic.route('')
# def topic_list():
#     topics = Topic.query.all()
#     return render_template('topic/list.html', topics=topics)


# @topic.route('/followed')
# def user_topics():
#     topics = current_user.topics_liked.all()
#     return render_template('topic/user.html', topics=topics)


# use slug instead of id
@topic.route('/<int:id>/')
def detail(id):
    topic = Topic.query.get_or_404(id)
    stories = topic.get_published_stories().all()
    return render_template('topic/detail.html',
                              topic=topic, stories=stories)


# @topic.route('/<int:id>/like')
# def like_topic(id):
#     topic = Topic.query.get_or_404(id)


# @login_required
# def like(request, id):
#     topic = get_object_or_404(Topic,
#         id=id)
#     current_url = request.META['HTTP_REFERER']
#     users_likes = topic.users_likes.filter(
#         username=request.user.username)
#     if not users_likes:
#         topic.likes += 1
#         topic.users_likes.add(request.user)
#         messages.success(request, "You've liked this topic.")
#         return redirect(current_url)
#     else:
#         return HttpResponseBadRequest()

# @ajax_required
# @login_required
# @require_POST
# def topic_like(request):
#     topic_id = request.POST.get('id')
#     action = request.POST.get('action')
#     if topic_id and action:
#         try:
#             topic = Topic.objects.get(id=topic_id)
#             if action == 'like':
#                 topic.users_like.add(request.user)
#             else:
#                 topic.users_like.remove(request.user)
#             return JsonResponse({'status': 'ok'})
#         except:
#             pass
#     return JsonResponse({'status': 'ko'})

# @login_required
# def unlike(request, id):
#     topic = get_object_or_404(Topic,
#         id=id)
#     current_url = request.META['HTTP_REFERER']
#     users_likes = topic.users_likes.filter(
#         username=request.user.username)
#     if users_likes:
#         topic.likes -= 1
#         topic.users_likes.remove(request.user)
#         messages.success(request, "You've unliked this topic.")
#         return redirect(current_url)
#     else:
#         return HttpResponseBadRequest()

