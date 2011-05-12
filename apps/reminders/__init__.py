import datetime

from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_menu, \
    register_model_list_columns, register_multi_item_links
from permissions.api import register_permissions
from common.utils import two_state_template

from reminders.models import Reminder, Participant

PERMISSION_REMINDER_VIEW = 'reminder_view'
PERMISSION_REMINDER_VIEW_ALL = 'reminder_view_all'
PERMISSION_REMINDER_CREATE = 'reminder_create'
PERMISSION_REMINDER_EDIT = 'reminder_edit'
PERMISSION_REMINDER_EDIT_ALL = 'reminder_edit_all'
PERMISSION_REMINDER_DELETE = 'reminder_delete'
PERMISSION_REMINDER_DELETE_ALL = 'reminder_delete_all'

register_permissions('reminders', [
    {'name': PERMISSION_REMINDER_VIEW, 'label': _(u'View reminder')},
    {'name': PERMISSION_REMINDER_VIEW_ALL, 'label': _(u'View all reminders')},
    {'name': PERMISSION_REMINDER_CREATE, 'label': _(u'Create reminder')},
    {'name': PERMISSION_REMINDER_EDIT, 'label': _(u'Edit reminder')},
    {'name': PERMISSION_REMINDER_EDIT_ALL, 'label': _(u'Edit all reminders')},
    {'name': PERMISSION_REMINDER_DELETE, 'label': _(u'Delete reminder')},
    {'name': PERMISSION_REMINDER_DELETE_ALL, 'label': _(u'Delete all reminders')},
])

reminder_list = {'text': _(u'reminder list'), 'view': 'reminder_list', 'famfam': 'hourglass', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_VIEW]}}
reminder_list_all = {'text': _(u'reminder list (all)'), 'view': 'reminder_list_all', 'famfam': 'hourglass', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_VIEW_ALL]}}
expired_remider_list = {'text': _(u'expired reminder list'), 'view': 'expired_remider_list', 'famfam': 'hourglass', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_VIEW]}}
expired_remider_list_all = {'text': _(u'expired reminder list (all)'), 'view': 'expired_remider_list_all', 'famfam': 'hourglass', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_VIEW_ALL]}}
reminder_add = {'text': _(u'create reminder (calendar)'), 'view': 'reminder_add', 'famfam': 'hourglass_add', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_CREATE]}}
reminder_add_days = {'text': _(u'create reminder (days)'), 'view': 'reminder_add_days', 'famfam': 'hourglass_add', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_CREATE]}}
reminder_edit = {'text': _(u'edit (calendar)'), 'view': 'reminder_edit', 'args': 'object.pk', 'famfam': 'hourglass_go', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_EDIT]}}
reminder_edit_days = {'text': _(u'edit (days)'), 'view': 'reminder_edit_days', 'args': 'object.pk', 'famfam': 'hourglass_go', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_EDIT]}}
future_expired_remider_list = {'text': _(u'future expired reminders'), 'view': 'future_expired_remider_list', 'famfam': 'hourglass', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_VIEW]}}
future_expired_remider_list_all = {'text': _(u'future expired reminders (all)'), 'view': 'future_expired_remider_list_all', 'famfam': 'hourglass', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_VIEW_ALL]}}

reminder_delete = {'text': _(u'delete'), 'view': 'reminder_delete', 'args': 'object.id', 'famfam': 'hourglass_delete', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_DELETE]}}
reminder_multiple_delete = {'text': _(u'delete'), 'view': 'reminder_multiple_delete', 'famfam': 'hourglass_delete', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_DELETE]}}

reminder_participant_add = {'text': _(u'add participant'), 'view': 'participant_add', 'args': 'object.pk', 'famfam': 'user_add', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_EDIT]}}
reminder_participant_remove = {'text': _(u'remove'), 'view': 'participant_remove', 'args': 'object.pk', 'famfam': 'user_delete', 'permissions': {'namespace': 'reminders', 'permissions': [PERMISSION_REMINDER_EDIT]}}

register_links(
    [
        'participant_remove', 'reminder_participant_add',
        'future_expired_remider_list', 'future_expired_remider_list_all',
        'reminder_view', 'reminder_list_all', 'reminder_edit',
        'reminder_edit_days', 'reminder_delete', 'reminder_list',
        'expired_remider_list', 'expired_remider_list_all', 'reminder_add',
        'reminder_add_days', 'participant_add'],
    [
        reminder_list, reminder_list_all, expired_remider_list,
        expired_remider_list_all, future_expired_remider_list, 
        future_expired_remider_list_all, reminder_add, reminder_add_days
    ], menu_name='sidebar'
)
register_links([Reminder],
    [
        reminder_edit, reminder_edit_days, reminder_participant_add,
        reminder_delete
    ]
)
register_links([Participant], [reminder_participant_remove])
register_multi_item_links(
    [
        'reminder_list', 'reminder_list_all', 'expired_remider_list',
        'expired_remider_list_all', 'future_expired_remider_list',
        'future_expired_remider_list_all'
    ],
    [
        reminder_multiple_delete
    ]
)

register_menu([
    {'text': _(u'reminders'), 'view': 'reminder_list', 'links': [
       # reminder_list, expired_remider_list, future_expired_remider_list
    ], 'famfam': 'hourglass', 'position': 1}])

register_model_list_columns(Reminder, [
        {
            'name': _(u'created'),
            'attribute': lambda x: x.datetime_created
        },
        {
            'name': _(u'expires'),
            'attribute': lambda x: x.datetime_expire
        },
        {
            'name': _('days'),
            'attribute': lambda x: (x.datetime_expire - x.datetime_created).days
        },
        {
            'name': _('expired?'),
            'attribute': lambda x: two_state_template((x.datetime_expire < datetime.datetime.now().date()), states=1)
        }	
    ])

register_model_list_columns(Participant, [
    {
        'name': _(u'name'),
        'attribute': lambda x: x.user.get_full_name() if x.user.get_full_name() else x.user
    },
    {
        'name': _(u'role'),
        'attribute': lambda x: x.get_role_display()
    }	
    ])
