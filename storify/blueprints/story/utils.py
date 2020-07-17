import re
import math
from django.utils.html import strip_tags


def count_words(html_string):
    word_string = strip_tags(html_string)
    count = len(re.findall(r'\w+', word_string))
    return count


def get_read_time(html_string):
    count = count_words(html_string)
    # round up value to the nearest minute. 200 wpm
    read_time_min = math.ceil(count // 200)
    return int(read_time_min)


def object_list(template_name, query, paginate_by=5, **context):
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    object_list = query.paginate(page, paginate_by)
    return render_template(template_name, object_list=object_list, **context)


def entry_list(template_name, query, **context):
    """ Filter results based on search query"""
    query = filter_status_by_user(query)
    valid_statuses = (Entry.DRAFT, Entry.PUBLISHED)
    query = query.filter(Entry.status.in_(valid_statuses))
    if request.args.get('q'):
        search = request.args['q']
        query = query.filter(
            (Entry.body.contains(search)) | (Entry.title.contains(search)))
    return object_list(template_name, query, **context)


def get_entry_or_404(slug, author=None):
    """
    Helper function used to extract entries from the database by the
    given slug.
    """
    query = Entry.query.filter(Entry.slug == slug)
    if author:
        query = query.filter(Entry.author == author)
    else:
        query = filter_status_by_user(query)
    return query.first_or_404()


def filter_status_by_user(query):
    """
    Helper function filter shown entries by the user status.
    Only published entries accessible for non authenticated users.
    """
    if not current_user.is_authenticated:
        query = query.filter(Entry.status == Entry.PUBLISHED)
    else:
        # Allow users to view their own drafts
        query = query.filter(
            (Entry.status == Entry.PUBLISHED) |
            ((Entry.author == current_user) &
                (Entry.status != Entry.DELETED)))
    return query
