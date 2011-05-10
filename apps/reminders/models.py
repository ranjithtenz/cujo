import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from dynamic_search.api import register


class Reminder(models.Model):
	label = models.CharField(max_length=64, verbose_name=_(u'label'))
	notes = models.TextField(blank=True, verbose_name=_(u'notes'))
	datetime_created = models.DateTimeField(blank=True, verbose_name=_(u'creation date'), default=datetime.datetime.now())
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
		



register(Reminder, _(u'reminder'), [u'label', 'notes'])
