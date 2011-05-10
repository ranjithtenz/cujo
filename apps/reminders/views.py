from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.views.generic.create_update import delete_object, update_object
from django.conf import settings
from django.utils.http import urlencode

from permissions.api import check_permissions

from reminders.forms import ReminderForm, ReminderForm_view
from reminders.models import Reminder
from reminders import PERMISSION_REMINDER_VIEW, PERMISSION_REMINDER_CREATE, \
	PERMISSION_REMINDER_EDIT, PERMISSION_REMINDER_DELETE


def reminder_list(request, object_list=None, title=None):
	check_permissions(request.user, 'reminders', [PERMISSION_REMINDER_VIEW])

	return render_to_response('generic_list.html', {
		'object_list': object_list if not (object_list is None) else Reminder.objects.all(),
		'title': title if title else _(u'reminders'),
		'multi_select_as_buttons': True,

	}, context_instance=RequestContext(request))


def reminder_add(request):
	check_permissions(request.user, u'reminders', [PERMISSION_REMINDER_CREATE])
	
	next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', u'/')))
	
	if request.method == 'POST':
		form = ReminderForm(request.POST)
		if form.is_valid():
			reminder = form.save()
			messages.success(request, _(u'Reminder "%s" added successfully.') % reminder)
			return HttpResponseRedirect(next)
	else:
		form = ReminderForm()
		
	return render_to_response('generic_form.html', {
		'title': _(u'Create reminder'),
		'form': form,
		'next': next,
	},
	context_instance=RequestContext(request))
	

def reminder_edit(request, reminder_id):
	check_permissions(request.user, u'reminders', [PERMISSION_REMINDER_EDIT])
	
	reminder = get_object_or_404(Reminder, pk=reminder_id)
	
	next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', u'/')))
	
	if request.method == 'POST':
		form = ReminderForm(instance=reminder, data=request.POST)
		if form.is_valid():
			reminder = form.save()
			messages.success(request, _(u'Reminder "%s" edited successfully.') % reminder)
			return HttpResponseRedirect(next)
	else:
		form = ReminderForm(instance=reminder)
		
	return render_to_response('generic_form.html', {
		'title': _(u'Edit reminder "%s"') % reminder,
		'form': form,
		'next': next,
		'object': reminder,
	},
	context_instance=RequestContext(request))


def reminder_delete(request, reminder_id=None, reminder_id_list=None):
    check_permissions(request.user, 'reminders', [PERMISSION_REMINDER_DELETE])
    post_action_redirect = None

    if reminder_id:
        reminders = [get_object_or_404(Reminder, pk=reminder_id)]
        #post_action_redirect = reverse('reminder_list')
    elif reminder_id_list:
        reminders = [get_object_or_404(Reminder, pk=reminder_id) for reminder_id in reminder_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one reminder.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for reminder in reminders:
            try:
                reminder.delete()
                messages.success(request, _(u'Reminder "%s" deleted successfully.') % reminder)
            except Exception, e:
                messages.error(request, _(u'Error deleting reminder "%(reminder)s"; %(error)s') % {
                    'reminder': reminder, 'error': e
                })

        return HttpResponseRedirect(next)
    context = {
        'object_name': _(u'reminder'),
        'delete_view': True,
        'previous': previous,
        'next': next,
    }
    if len(reminders) == 1:
        context['object'] = reminders[0]
        context['title'] = _(u'Are you sure you wish to delete the reminder "%s"?') % ', '.join([unicode(d) for d in reminders])
    elif len(reminders) > 1:
        context['title'] = _(u'Are you sure you wish to delete the reminders: %s?') % ', '.join([unicode(d) for d in reminders])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def reminder_multiple_delete(request):
    return reminder_delete(
        request, reminder_id_list=request.GET.get('id_list', [])
    )

def reminder_view(request, reminder_id):
	check_permissions(request.user, u'reminders', [PERMISSION_REMINDER_VIEW])
	
	reminder = get_object_or_404(Reminder, pk=reminder_id)

	form = ReminderForm_view(instance=reminder)
		
	return render_to_response('generic_form.html', {
		'title': _(u'Detail for reminder "%s"') % reminder,
		'form': form,
		'object': reminder,
	},
	context_instance=RequestContext(request))
