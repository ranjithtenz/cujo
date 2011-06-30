from django.utils.translation import ugettext_lazy as _

from navigation.api import register_menu
from permissions import role_list
from user_management import user_list, group_list
from permissions.api import register_permission, set_namespace_title

from main.conf.settings import SIDE_BAR_SEARCH

PERMISSION_MAIN_TOOLS = {'namespace': 'main', 'name': 'main_tools', 'label': _(u'Can access tools menu')}
PERMISSION_MAIN_SETUP = {'namespace': 'main', 'name': 'main_setup', 'label': _(u'Can access setup menu')}

set_namespace_title('main', _(u'Main'))
register_permission(PERMISSION_MAIN_TOOLS)
register_permission(PERMISSION_MAIN_SETUP)


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser

check_settings = {'text': _(u'settings'), 'view': 'setting_list', 'famfam': 'cog'}
#statistics = {'text': _(u'statistics'), 'view': 'statistics', 'famfam': 'table'}
#diagnostics = {'text': _(u'diagnostics'), 'view': 'diagnostics', 'famfam': 'pill'}
tools = {'text': _(u'tools'), 'view': 'tools_menu', 'famfam': 'wrench', 'permissions': [PERMISSION_MAIN_TOOLS]}
admin_site = {'text': _(u'admin site'), 'url': '/admin', 'famfam': 'keyboard', 'condition': is_superuser}
sentry = {'text': _(u'sentry'), 'url': '/sentry', 'famfam': 'bug', 'condition': is_superuser}


__version_info__ = {
    'major': 0,
    'minor': 2,
    'micro': 0,
    'releaselevel': 'final',
    'serial': 0
}

main_menu = [
    {'text': _(u'home'), 'view': 'home', 'famfam': 'house', 'position': 0},
    {'text': _(u'tools'), 'view': 'tools_menu', 'links': [
        #tools, statistics, diagnostics, sentry
        tools, sentry
        ], 'famfam': 'wrench', 'name': 'tools', 'position': 7, 'permissions': [PERMISSION_MAIN_TOOLS]},

    {'text': _(u'setup'), 'view': 'setting_list', 'links': [
        check_settings, role_list, user_list, group_list, admin_site
        ], 'famfam': 'cog', 'name': 'setup', 'position': 8, 'permissions': [PERMISSION_MAIN_SETUP]},

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
