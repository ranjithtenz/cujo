"""Configuration options for the reminders app"""

from django.utils.translation import ugettext_lazy as _
from smart_settings.api import register_setting

register_setting(
    namespace=u'reminders',
    module=u'reminders.conf.settings',
    name=u'CHECK_PROCESSING_INTERVAL',
    global_name=u'REMINDERS_CHECK_PROCESSING_INTERVAL',
    default=60,
    description=_(u'Interval in seconds to wait before checking for expired reminders.')
)
