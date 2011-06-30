import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from dynamic_search.api import register

PARTICIPANT_ROLE_CREATOR = u'cr'
PARTICIPANT_ROLE_WATCHER = u'wa'
PARTICIPANT_ROLE_EDITOR = u'ed'

PARTICIPANT_ROLE_CHOICES = (
    (PARTICIPANT_ROLE_CREATOR, _(u'Creator')),
    (PARTICIPANT_ROLE_EDITOR, _(u'Editor')),
    (PARTICIPANT_ROLE_WATCHER, _(u'Watcher')),
)


class Reminder(models.Model):
    label = models.CharField(max_length=64, verbose_name=_(u'label'))
    notes = models.TextField(blank=True, verbose_name=_(u'notes'))
    datetime_created = models.DateField(blank=True, verbose_name=_(u'creation date'), default=datetime.datetime.now())
    datetime_expire = models.DateField(verbose_name=_(u'expiration date'))

    class Meta:
        ordering = ('-datetime_created',)
        verbose_name = _(u'reminder')
        verbose_name_plural = _(u'reminders')

    def __unicode__(self):
        return self.label

    @models.permalink
    def get_absolute_url(self):
        return ('reminder_view', [self.pk])

    def save(self, *args, **kwargs):
        new_instance = not self.pk
        if new_instance:
            if not self.datetime_created:
                self.datetime_created = datetime.datetime.now()

        super(Reminder, self).save(*args, **kwargs)


class Participant(models.Model):
    reminder = models.ForeignKey(Reminder, verbose_name=_(u'reminder'))
    user = models.ForeignKey(User, verbose_name=_(u'user'))
    role = models.CharField(max_length=2, choices=PARTICIPANT_ROLE_CHOICES, verbose_name=_(u'role'))

    class Meta:
        unique_together = ('reminder', 'user', 'role')
        verbose_name = _(u'participant')
        verbose_name_plural = _(u'participants')

    def __unicode__(self):
        return unicode(self.user.get_full_name() if self.user.get_full_name() else self.user)


PREEMPTIVE_CHOICES = (
    (u'48h', _(u'2 days')),
    (u'24h', _(u'1 day')),
    (u'12h', _(u'12 hours')),
    (u'6h', _(u'6 hours')),
    (u'2h', _(u'2 hours')),
    (u'1h', _(u'1 hour')),
    (u'30m', _(u'30 minutes')),
    (u'15m', _(u'15 minutes')),
)

REPETITION_CHOICES = (
    (u'24h', _(u'1 day')),
    (u'12h', _(u'12 hours')),
    (u'6h', _(u'6 hours')),
    (u'2h', _(u'2 hours')),
    (u'1h', _(u'1 hour')),
    (u'30m', _(u'30 minutes')),
    (u'15m', _(u'15 minutes')),
)


class Notification(models.Model):
    reminder = models.ForeignKey(Reminder, verbose_name=_(u'reminder'))
    participant = models.ForeignKey(Participant, verbose_name=_(u'participant'))
    preemptive = models.CharField(max_length=4, choices=PREEMPTIVE_CHOICES, verbose_name=_(u'preemptive'))

    class Meta:
        verbose_name = _(u'notification')
        verbose_name_plural = _(u'notifications')

    def __unicode__(self):
        return self.label


register(Reminder, _(u'reminder'), [u'label', 'notes', 'participant__user__username', 'participant__user__first_name', 'participant__user__last_name'])
