from ...extensions import db


class Notification(db.Model):
    COMMENTED = 'CO'
    ALSO_COMMENTED = 'AC'
    FAVORITED = 'FA'
    FOLLOWED = 'FO'
    NOTIFICATION_TYPES = (
        (COMMENTED, 'Commented'),
        (ALSO_COMMENTED, 'Also Commented'),
        (FAVORITED, 'Favorited'),
        (FOLLOWED, 'Followed'),
    )

    _COMMENTED_TEMPLATE = '''
        <div class="profile-notification-body">
            <a href="{0}" class="link-to"></a>
            <p><span class="primary">{1}</span> commented on your story <span>{2}</span>.</p>
        </div>
        <div class="profile-notification-type">
            <span class="type-icon icon-speech primary"></span>
        </div>
    '''
    _ALSO_COMMENTED_TEMPLATE = '''
        <div class="profile-notification-body">
            <a href="{0}" class="link-to"></a>
            <p><span class="primary">{1}</span> also commented on the story <span>{2}</span>.</p>
        </div>
        <div class="profile-notification-type">
            <span class="type-icon icon-bubble primary"></span>
        </div>
    '''
    _FAVORITED_TEMPLATE = '''
        <div class="profile-notification-body">
            <a href="{0}" class="link-to"></a>
            <p><span class="primary">{1}</span> favorited your story <span>{2}</span>.</p>
        </div>
        <div class="profile-notification-type">
            <span class="type-icon icon-heart primary"></span>
        </div>
    '''
    _FOLLOWED_TEMPLATE = '''
        <div class="profile-notification-body">
            <a href="{0}" class="link-to"></a>
            <p><span class="primary">{1}</span> started following you.</p>
        </div>
        <div class="profile-notification-type">
            <span class="type-icon icon-user-following primary"></span>
        </div>
    '''

    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    created = models.DateTimeField(auto_now_add=True)
    story = models.ForeignKey('story.Story', null=True, blank=True)
    follow = models.ForeignKey('accounts.Follow', null=True, blank=True)
    notification_type = models.CharField(max_length=2, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created']

    def __str__(self):
        if self.notification_type == self.COMMENTED:
            return self._COMMENTED_TEMPLATE.format(
                self.story.get_absolute_url(),
                escape(self.from_user.profile.get_screen_name()),
                escape(self.get_summary(self.story.title)),
            )
        elif self.notification_type == self.ALSO_COMMENTED:
            return self._ALSO_COMMENTED_TEMPLATE.format(
                self.story.get_absolute_url(),
                escape(self.from_user.profile.get_screen_name()),
                escape(self.get_summary(self.story.title)),
            )
        elif self.notification_type == self.FAVORITED:
            return self._FAVORITED_TEMPLATE.format(
                self.story.get_absolute_url(),
                escape(self.from_user.profile.get_screen_name()),
                escape(self.get_summary(self.story.title)),
            )
        elif self.notification_type == self.FOLLOWED:
            return self._FOLLOWED_TEMPLATE.format(
                escape(self.from_user.get_absolute_url()),
                escape(self.from_user.profile.get_screen_name()),
            )
        else:
            return 'Ooops! Something went wrong.'

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return '{0}...'.format(value[:summary_size])

        else:
            return value
