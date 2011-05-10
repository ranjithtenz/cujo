from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('reminders.views',
    url(r'^list/$', 'reminder_list', (), 'reminder_list'),
    url(r'^add/$', 'reminder_add', (), 'reminder_add'),
    url(r'^edit/(?P<reminder_id>\d+)/$', 'reminder_edit', (), 'reminder_edit'),
    url(r'^(?P<reminder_id>\d+)/$', 'reminder_view', (), 'reminder_view'),
    url(r'^(?P<reminder_id>\d+)/delete/$', 'reminder_delete', (), 'reminder_delete'),
    url(r'^multiple/delete/$', 'reminder_multiple_delete', (), 'reminder_multiple_delete'),


)
