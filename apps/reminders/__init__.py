from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from navigation.api import register_links, register_menu, \
    register_model_list_columns, register_multi_item_links
from main.api import register_diagnostic, register_tool
from permissions.api import register_permissions

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
reminder_add = {'text': _(u'add reminder'), 'view': 'reminder_add', 'famfam': 'hourglass_add', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_CREATE]}}
reminder_edit = {'text': _(u'edit'), 'view': 'reminder_edit', 'args': 'object.pk', 'famfam': 'hourglass_go', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_EDIT]}}

reminder_delete = {'text': _(u'delete'), 'view': 'reminder_delete', 'args': 'object.id', 'famfam': 'hourglass_delete', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_DELETE]}}
reminder_multiple_delete = {'text': _(u'delete'), 'view': 'reminder_multiple_delete', 'famfam': 'hourglass_delete', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_DELETE]}}

register_links(['reminder_edit', 'reminder_delete', 'reminder_list', 'reminder_add'], [reminder_list, reminder_add], menu_name='sidebar')
register_links([Reminder], [reminder_edit, reminder_delete])
register_multi_item_links(['reminder_list'], [reminder_multiple_delete])

register_menu([
	{'text': _(u'reminders'), 'view': 'reminder_list', 'links': [
		reminder_list
	], 'famfam': 'hourglass', 'position': 1}])

register_model_list_columns(Reminder, [
	{
		'name': _(u'Creation date'),
		'attribute': lambda x: x.datetime_created.date()
	},
	{
		'name': _(u'Expiration date'),
		'attribute': lambda x: x.datetime_created.date()
	}	
    ])
