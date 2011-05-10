from datetime import timedelta

from django.utils.translation import ugettext_lazy as _

from celery.decorators import task, periodic_task

from reminders.conf.settings import CHECK_PROCESSING_INTERVAL


@periodic_task(run_every=timedelta(seconds=CHECK_PROCESSING_INTERVAL))
def task_check_for_expired_reminders():
	pass
