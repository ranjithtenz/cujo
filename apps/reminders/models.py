import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from dynamic_search.api import register


class Reminder(models.Model):
	label = models.CharField(max_length=64, verbose_name=_(u'label'))
	notes = models.TextField(blank=True, verbose_name=_(u'notes'))
	datetime_created = models.DateField(blank=True, verbose_name=_(u'creation date'), default=datetime.datetime.now())
	datetime_expire = models.DateField(verbose_name=_(u'expiration date'))
	
	class Meta:
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
	
	class Meta:
		verbose_name = _(u'participant')
		verbose_name_plural = _(u'participants')
		
	def __unicode__(self):
		return u'%s - %s' % (self.reminder, self.user)


register(Reminder, _(u'reminder'), [u'label', 'notes', 'participant__user__username', 'participant__user__first_name', 'participant__user__last_name'])
