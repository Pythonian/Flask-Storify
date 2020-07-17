@app.route('/tags/')
def tags():
    # List tags with only one or more queries
    # Tag.query.join(entry_tags).distinct()
    # Display the number of entries in each tag
    tags = Tag.query.order_by(Tag.name)
    return object_list('tags.html', tags)


@app.route('/tag/<slug>/')
def tag(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    entries = tag.entries.order_by(Entry.created.desc())
    return object_list('tag.html', entries, tag=tag)
