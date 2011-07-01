from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu, register_links
from permissions import role_list, permission_views
from user_management import user_list, group_list, user_management_views
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
statistics = {'text': _(u'statistics'), 'view': 'statistics', 'famfam': 'table'}
diagnostics = {'text': _(u'diagnostics'), 'view': 'diagnostics', 'famfam': 'pill'}
tools_menu = {'text': _(u'tools'), 'view': 'tools_menu', 'famfam': 'wrench'}
admin_site = {'text': _(u'admin site'), 'url': '/admin', 'famfam': 'keyboard', 'condition': is_superuser}
sentry = {'text': _(u'sentry'), 'url': '/sentry', 'famfam': 'bug', 'condition': is_superuser}


register_top_menu('home', link={'text': _(u'home'), 'view': 'home', 'famfam': 'house'}, position=0)
if not SIDE_BAR_SEARCH:
    register_top_menu('search', link={'text': _(u'search'), 'view': 'search', 'famfam': 'zoom'}, children_path_regex=[r'^search/'])

register_top_menu('setup_menu', link={'text': _(u'setup'), 'view': 'setting_list', 'famfam': 'cog'}, children_path_regex=[r'^settings/', r'^user_management/', r'^permissions', r'^documents/type', r'^metadata/setup'])

register_top_menu('about', link={'text': _(u'about'), 'view': 'about', 'famfam': 'information'})

setup_links = [check_settings, role_list, user_list, group_list, admin_site]
register_links(['setting_list'], setup_links, menu_name='secondary_menu')
register_links(permission_views, setup_links, menu_name='secondary_menu')
register_links(user_management_views, setup_links, menu_name='secondary_menu')


__version_info__ = {
    'major': 0,
    'minor': 2,
    'micro': 0,
    'releaselevel': 'final',
    'serial': 0
}


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
