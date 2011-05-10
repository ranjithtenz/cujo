import datetime

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from navigation.api import register_links, register_menu, \
    register_model_list_columns, register_multi_item_links
from main.api import register_diagnostic, register_tool
from permissions.api import register_permissions
from common.utils import two_state_template

from reminders.models import Reminder

PERMISSION_REMINDER_VIEW = 'reminder_view'
PERMISSION_REMINDER_CREATE = 'reminder_create'
PERMISSION_REMINDER_EDIT = 'reminder_edit'
PERMISSION_REMINDER_DELETE = 'reminder_delete'

register_permissions('reminders', [
    {'name': PERMISSION_REMINDER_VIEW, 'label': _(u'View reminder')},
    {'name': PERMISSION_REMINDER_CREATE, 'label': _(u'Create reminder')},
    {'name': PERMISSION_REMINDER_EDIT, 'label': _(u'Edit reminder')},
    {'name': PERMISSION_REMINDER_DELETE, 'label': _(u'Delete reminder')},
])

reminder_list = {'text': _(u'reminder list'), 'view': 'reminder_list', 'famfam': 'hourglass', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_VIEW]}}
expired_remider_list = {'text': _(u'expired reminder list'), 'view': 'expired_remider_list', 'famfam': 'hourglass', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_VIEW]}}
reminder_add = {'text': _(u'create reminder (calendar)'), 'view': 'reminder_add', 'famfam': 'hourglass_add', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_CREATE]}}
reminder_add_days = {'text': _(u'create reminder (days)'), 'view': 'reminder_add_days', 'famfam': 'hourglass_add', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_CREATE]}}
reminder_edit = {'text': _(u'edit (calendar)'), 'view': 'reminder_edit', 'args': 'object.pk', 'famfam': 'hourglass_go', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_EDIT]}}
reminder_edit_days = {'text': _(u'edit (days)'), 'view': 'reminder_edit_days', 'args': 'object.pk', 'famfam': 'hourglass_go', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_EDIT]}}

reminder_delete = {'text': _(u'delete'), 'view': 'reminder_delete', 'args': 'object.id', 'famfam': 'hourglass_delete', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_DELETE]}}
reminder_multiple_delete = {'text': _(u'delete'), 'view': 'reminder_multiple_delete', 'famfam': 'hourglass_delete', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_DELETE]}}

register_links(['reminder_view', 'reminder_edit', 'reminder_edit_days', 'reminder_delete', 'reminder_list', 'expired_remider_list', 'reminder_add', 'reminder_add_days'], [reminder_list, expired_remider_list, reminder_add, reminder_add_days], menu_name='sidebar')
register_links([Reminder], [reminder_edit, reminder_edit_days, reminder_delete])
register_multi_item_links(['reminder_list'], [reminder_multiple_delete])

register_menu([
	{'text': _(u'reminders'), 'view': 'reminder_list', 'links': [
		reminder_list, expired_remider_list, reminder_add, reminder_add_days
	], 'famfam': 'hourglass', 'position': 1}])

register_model_list_columns(Reminder, [
		{
			'name': _(u'creation date'),
			'attribute': lambda x: x.datetime_created.date()
		},
		{
			'name': _(u'expiration date'),
			'attribute': lambda x: x.datetime_expire
		},
		{
			'name': _('days'),
			'attribute': lambda x: (x.datetime_expire - x.datetime_created.date()).days
		},
		{
			'name': _('expired?'),
			'attribute': lambda x: two_state_template((x.datetime_expire < datetime.datetime.now().date()), states=1)
		}	
    ])
