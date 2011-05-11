from django.utils.translation import ugettext_lazy as _

from navigation.api import register_menu
from permissions import role_list
from user_management import user_list, group_list
from permissions.api import register_permissions

from main.conf.settings import SIDE_BAR_SEARCH

PERMISSION_MAIN_TOOLS = 'main_tools'
PERMISSION_MAIN_SETUP = 'main_setup'

register_permissions('main', [
    {'name': PERMISSION_MAIN_TOOLS, 'label': _(u'Can access tools menu')},
    {'name': PERMISSION_MAIN_SETUP, 'label': _(u'Can access setup menu')},
])


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser

check_settings = {'text': _(u'settings'), 'view': 'setting_list', 'famfam': 'cog'}
#statistics = {'text': _(u'statistics'), 'view': 'statistics', 'famfam': 'table'}
#diagnostics = {'text': _(u'diagnostics'), 'view': 'diagnostics', 'famfam': 'pill'}
tools = {'text': _(u'tools'), 'view': 'tools_menu', 'famfam': 'wrench', 'permissions': {'namespace': 'main', 'permissions': [PERMISSION_MAIN_TOOLS]}}
admin_site = {'text': _(u'admin site'), 'url': '/admin', 'famfam': 'keyboard', 'condition': is_superuser}
sentry = {'text': _(u'sentry'), 'url': '/sentry', 'famfam': 'bug', 'condition': is_superuser}


__version_info__ = {
    'major': 0,
    'minor': 1,
    'micro': 5,
    'releaselevel': 'final',
    'serial': 0
}

main_menu = [
    {'text': _(u'home'), 'view': 'home', 'famfam': 'house', 'position': 0},
    {'text': _(u'tools'), 'view': 'tools_menu', 'links': [
        #tools, statistics, diagnostics, sentry
        tools, sentry
        ], 'famfam': 'wrench', 'name': 'tools', 'position': 7, 'permissions': {'namespace': 'main', 'permissions': [PERMISSION_MAIN_TOOLS]}},

    {'text': _(u'setup'), 'view': 'setting_list', 'links': [
        check_settings, role_list, user_list, group_list, admin_site
        ], 'famfam': 'cog', 'name': 'setup', 'position': 8, 'permissions': {'namespace': 'main', 'permissions': [PERMISSION_MAIN_SETUP]}},

    {'text': _(u'about'), 'view': 'about', 'position': 9},
]

if not SIDE_BAR_SEARCH:
    main_menu.insert(1, {'text': _(u'search'), 'view': 'search', 'famfam': 'zoom', 'position': 2})

register_menu(main_menu)


def get_version():
    """
    Return the formatted version information
    """
    vers = ["%(major)i.%(minor)i" % __version_info__, ]

    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final':
        vers.append('%(releaselevel)s%(serial)i' % __version_info__)
    return ''.join(vers)

__version__ = get_version()
