import datetime

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.utils import formats
#from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment

from permissions.api import check_permissions
from reminder_comments.utils import get_comments_subtemplate

from reminders.forms import ReminderForm, ReminderForm_view, \
    ReminderForm_days, FutureDateForm, ParticipantForm_add
from reminders.models import Reminder, Participant, \
    PARTICIPANT_ROLE_CHOICES, PARTICIPANT_ROLE_CREATOR, \
    PARTICIPANT_ROLE_EDITOR, PARTICIPANT_ROLE_WATCHER
from reminders import PERMISSION_REMINDER_VIEW, PERMISSION_REMINDER_CREATE, \
    PERMISSION_REMINDER_EDIT, PERMISSION_REMINDER_DELETE, \
    PERMISSION_REMINDER_VIEW_ALL, PERMISSION_REMINDER_EDIT_ALL, \
    PERMISSION_REMINDER_DELETE_ALL
from reminders.utils import get_user_full_name


def reminder_list(request, object_list=None, title=None, view_all=False):
    if view_all:
        check_permissions(request.user, 'reminders', [PERMISSION_REMINDER_VIEW_ALL])
        query_set = Reminder.objects.all()
    else:
        check_permissions(request.user, 'reminders', [PERMISSION_REMINDER_VIEW])
        query_set = Reminder.objects.filter(participant__user=request.user)

    return render_to_response('generic_list.html', {
        'object_list': object_list if not (object_list is None) else query_set,
        'title': title if title else _(u'reminders %s') % (_(u'(all)') if view_all else u''),
        'multi_select_as_buttons': True,
        'hide_links': True,

    }, context_instance=RequestContext(request))


def reminder_add(request, form_class=ReminderForm):
    check_permissions(request.user, u'reminders', [PERMISSION_REMINDER_CREATE])

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', u'/')))

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            if form_class == ReminderForm_days:
                reminder = form.save(commit=False)
                reminder.datetime_expire = reminder.datetime_created + datetime.timedelta(days=int(form.cleaned_data['days']))
                reminder.save()
            else:
                reminder = form.save()

            participant = Participant(reminder=reminder, user=request.user, role=PARTICIPANT_ROLE_CREATOR)
            participant.save()
            messages.success(request, _(u'Reminder "%s" created successfully.') % reminder)
            return HttpResponseRedirect(reverse('reminder_list'))
    else:
        form = form_class()

    return render_to_response('generic_form.html', {
        'title': _(u'create reminder (%s)') % (_(u'calendar') if form_class == ReminderForm else _(u'days')),
        'form': form,
        'next': next,
    },
    context_instance=RequestContext(request))


def reminder_edit(request, reminder_id, form_class=ReminderForm):
    try:
        check_permissions(request.user, 'reminders', [PERMISSION_REMINDER_EDIT_ALL])
        reminder = get_object_or_404(Reminder, pk=reminder_id)
    except PermissionDenied:
        check_permissions(request.user, u'reminders', [PERMISSION_REMINDER_EDIT])
        try:
            reminder = get_object_or_404(Reminder.objects.filter(participant__user=request.user).filter(participant__role__in=[PARTICIPANT_ROLE_CREATOR, PARTICIPANT_ROLE_EDITOR]), pk=reminder_id)
        except Http404:
            raise PermissionDenied

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', u'/')))

    if request.method == 'POST':
        form = form_class(instance=reminder, data=request.POST)
        if form.is_valid():
            if form_class == ReminderForm_days:
                reminder = form.save(commit=False)
                reminder.datetime_expire = reminder.datetime_created + datetime.timedelta(days=int(form.cleaned_data['days']))
                reminder.save()
            else:
                reminder = form.save()
            messages.success(request, _(u'Reminder "%s" edited successfully.') % reminder)
            return HttpResponseRedirect(reverse('reminder_list'))
    else:
        form = form_class(instance=reminder)

    expired = (datetime.datetime.now().date() - reminder.datetime_expire).days
    expired_template = _(u'(expired %s days)') % expired
    subtemplates_list = [
        {
            'name': 'generic_form_subtemplate.html',
            'context': {
            'title': _(u'Edit reminder "%(reminder)s" %(expired)s') % {
                'reminder': reminder, 'expired': expired_template if expired > 0 else u''},
                    'form': form,
             }
        },
        {
            'name': 'generic_list_subtemplate.html',
            'context': {
                'object_list': reminder.participant_set.all(),
                'title': _(u'participants'),
                'hide_link': True,
                'hide_object': True,
             }
        },
    ]

    return render_to_response('generic_form.html', {
        'title': _(u'Edit reminder "%s"') % reminder,
        #'form': form,
        'subtemplates_list': subtemplates_list,
        'next': next,
        'object': reminder,
    },
    context_instance=RequestContext(request))


def reminder_delete(request, reminder_id=None, reminder_id_list=None):
    check_permissions(request.user, 'reminders', [PERMISSION_REMINDER_DELETE])
    post_action_redirect = None

    if reminder_id:
        try:
            check_permissions(request.user, 'reminders', [PERMISSION_REMINDER_DELETE_ALL])
            reminders = [get_object_or_404(Reminder, pk=reminder_id)]
        except PermissionDenied:
            check_permissions(request.user, u'reminders', [PERMISSION_REMINDER_DELETE])
            try:
                reminders = [get_object_or_404(Reminder.objects.filter(participant__user=request.user).filter(participant__role__in=[PARTICIPANT_ROLE_CREATOR, PARTICIPANT_ROLE_EDITOR]).distinct(), pk=reminder_id)]
            except Http404:
                raise PermissionDenied

        post_action_redirect = reverse('reminder_list')
    elif reminder_id_list:
        # TODO: Improve to display PermissionDenied instead of 404 on unauthorized id's
        try:
            check_permissions(request.user, 'reminders', [PERMISSION_REMINDER_DELETE_ALL])
            reminders = [get_object_or_404(Reminder, pk=reminder_id) for reminder_id in reminder_id_list.split(',')]
        except PermissionDenied:
            check_permissions(request.user, 'reminders', [PERMISSION_REMINDER_DELETE])
            reminders = [get_object_or_404(Reminder.objects.filter(participant__user=request.user).filter(participant__role__in=[PARTICIPANT_ROLE_CREATOR, PARTICIPANT_ROLE_EDITOR]).distinct(), pk=reminder_id) for reminder_id in reminder_id_list.split(u',')]
    else:
        messages.error(request, _(u'Must provide at least one reminder.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', u'/')))
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
    try:
        check_permissions(request.user, 'reminders', [PERMISSION_REMINDER_VIEW_ALL])
        reminder = get_object_or_404(Reminder, pk=reminder_id)
    except PermissionDenied:
        check_permissions(request.user, u'reminders', [PERMISSION_REMINDER_VIEW])
        try:
            reminder = get_object_or_404(Reminder.objects.filter(participant__user=request.user).filter(participant__role__in=[PARTICIPANT_ROLE_CREATOR, PARTICIPANT_ROLE_EDITOR, PARTICIPANT_ROLE_WATCHER]).distinct(), pk=reminder_id)
        except Http404:
            raise PermissionDenied

    expired = (datetime.datetime.now().date() - reminder.datetime_expire).days
    expired_template = _(u' (expired %s days)') % expired

    form = ReminderForm_view(instance=reminder, extra_fields=[
        {'label': _(u'Days'), 'field': lambda x: (x.datetime_expire - x.datetime_created).days},
    ])

    subtemplates_list=[
        {
            'name': 'generic_detail_subtemplate.html',
            'context': {
            'title': _(u'Detail for reminder "%(reminder)s"%(expired)s') % {
                'reminder': reminder, 'expired': expired_template if expired > 0 else u''},
                    'form': form,
             }
        },
        {
            'name': 'generic_list_subtemplate.html',
            'context': {
                'object_list': reminder.participant_set.all(),
                'title': _(u'participants'),
                'hide_link': True,
                'hide_object': True,
             }
        },
    ]

    if Comment.objects.for_model(reminder).count():
        subtemplates_list.append(get_comments_subtemplate(reminder))
        
    return render_to_response('generic_detail.html', {
        'subtemplates_list': subtemplates_list,
        'object': reminder,
        'reminder': reminder
    },
    context_instance=RequestContext(request))


def expired_remider_list(request, expiration_date=datetime.datetime.now().date(), view_all=False):
    if view_all:
        check_permissions(request.user, 'reminders', [PERMISSION_REMINDER_VIEW_ALL])
        expired_reminders = Reminder.objects.filter(datetime_expire__lt=expiration_date)
    else:
        check_permissions(request.user, 'reminders', [PERMISSION_REMINDER_VIEW])
        expired_reminders = Reminder.objects.filter(participant__user=request.user).filter(datetime_expire__lt=expiration_date)

    return render_to_response('generic_list.html', {
        'object_list': expired_reminders.order_by('datetime_expire'),
        'title': _(u'expired reminders to the date: %(date)s %(all)s') % {
            'date': formats.date_format(expiration_date, u'DATE_FORMAT'),
            'all': _(u'(all)') if view_all else u''
            },
        'multi_select_as_buttons': True,
        'hide_links': True,
        'extra_columns': [
            {
                'name': _('days expired'),
                'attribute': lambda x: (expiration_date - x.datetime_expire).days
            }
        ]
    }, context_instance=RequestContext(request))


def future_expired_remider_list(request, view_all=False):
    check_permissions(request.user, u'reminders', [PERMISSION_REMINDER_VIEW, PERMISSION_REMINDER_VIEW_ALL])

    #next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', u'/')))

    if request.method == 'POST':
        form = FutureDateForm(request.POST)
        if form.is_valid():
            return expired_remider_list(request, expiration_date=form.cleaned_data['future_date'], view_all=view_all)
    else:
        form = FutureDateForm()
        
    return render_to_response('generic_form.html', {
        'title': _(u'Future expired reminders'),
        'form': form,
        #'next': next,
    },
    context_instance=RequestContext(request))


def participant_add(request, reminder_id):
    
    try:
        check_permissions(request.user, 'reminders', [PERMISSION_REMINDER_EDIT_ALL])
        reminder = get_object_or_404(Reminder, pk=reminder_id)
    except PermissionDenied:
        check_permissions(request.user, u'reminders', [PERMISSION_REMINDER_EDIT])
        try:
            reminder = get_object_or_404(Reminder.objects.filter(participant__user=request.user).filter(participant__role__in=[PARTICIPANT_ROLE_CREATOR, PARTICIPANT_ROLE_EDITOR]).distinct(), pk=reminder_id)
        except Http404:
            raise PermissionDenied

    if request.method == 'POST':
        form = ParticipantForm_add(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, pk=form.cleaned_data['user'])
            role = form.cleaned_data['role']
            # TODO: Don't allow creator/editor to downgrade himself if thereare no other creators/editors
            #if user == request.user and reminder.participant_set.filter(user=request.user).role == PARTICIPANT_ROLE_CREATOR and
            participant, created = Participant.objects.get_or_create(reminder=reminder, user=user)
            participant.role = role
            participant.save()

            messages.success(request, _(u'User: %(user)s added as reminder %(role)s.') % {
                'user': get_user_full_name(user), 'role': dict(PARTICIPANT_ROLE_CHOICES)[role]})
            return HttpResponseRedirect(reverse('reminder_view', args=[reminder.pk]))
    else:
        form = ParticipantForm_add()

    return render_to_response('generic_form.html', {
        'title': _(u'Add participant to the reminder "%s"') % reminder,
        'form': form,
        'object': reminder,
        #'next': next,
    },
    context_instance=RequestContext(request))	


def participant_remove(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id)
    reminder_id = participant.reminder_id
    try:
        check_permissions(request.user, 'reminders', [PERMISSION_REMINDER_EDIT_ALL])
        reminder = get_object_or_404(Reminder, pk=reminder_id)
    except PermissionDenied:
        check_permissions(request.user, u'reminders', [PERMISSION_REMINDER_EDIT])
        try:
            reminder = get_object_or_404(Reminder.objects.filter(participant__user=request.user).filter(participant__role__in=[PARTICIPANT_ROLE_CREATOR, PARTICIPANT_ROLE_EDITOR]).distinct(), pk=reminder_id)
        except Http404:
            raise PermissionDenied

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', u'/')))
    
    if participant.role == PARTICIPANT_ROLE_CREATOR:
        messages.error(request, _(u'Cannot remove reminder creator.'))
        return HttpResponseRedirect(previous)

    if request.method == 'POST':
        participant.delete()
        messages.success(request, _(u'Participant %(participant)s removed from reminder.') % {
            'participant': participant})

        return HttpResponseRedirect(reverse('reminder_view', args=[reminder.pk]))

    context = {
        'object_name': _(u'participant'),
        'delete_view': True,
        'previous': previous,
        #'next': next,
    }
    context['object'] = participant
    context['title'] = _(u'Are you sure you wish to remove the participant "%s"?') % participant

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))
