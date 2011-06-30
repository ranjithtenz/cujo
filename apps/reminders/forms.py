import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User

from common.forms import DetailForm

from reminders.models import Reminder, \
    PARTICIPANT_ROLE_EDITOR, PARTICIPANT_ROLE_WATCHER
from reminders.utils import get_user_full_name

ALLOWED_PARTICIPANT_ROLE_CHOICES = (
    (PARTICIPANT_ROLE_EDITOR, _(u'Editor')),
    (PARTICIPANT_ROLE_WATCHER, _(u'Watcher')),
)


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder

    def __init__(self, *args, **kwargs):
        super(ReminderForm, self).__init__(*args, **kwargs)
        self.fields['notes'].widget.attrs.update({'rows': 4})
        self.fields['datetime_expire'].initial = self.fields['datetime_created'].initial.date()
        self.fields['datetime_expire'].widget = SelectDateWidget()
        self.fields['datetime_created'].widget = SelectDateWidget()


class ReminderForm_days(ReminderForm):
    class Meta:
        model = Reminder

    def __init__(self, *args, **kwargs):
        super(ReminderForm_days, self).__init__(*args, **kwargs)
        self.fields['datetime_expire'].required = False
        self.fields['datetime_expire'].widget = forms.widgets.HiddenInput()
        self.fields['datetime_expire'].initial = self.fields['datetime_created'].initial.date()

        if self.instance.datetime_created and self.instance.datetime_expire:
            self.fields['days'].initial = (self.instance.datetime_expire - self.instance.datetime_created).days

    days = forms.CharField(label=_(u'Expiration days'), widget=forms.widgets.TextInput(attrs={'maxlength': '4', 'class': 'short_textbox'}))
    #HACK
    datetime_expire = forms.CharField(required=False)


class ReminderForm_view(DetailForm):
    class Meta:
        model = Reminder


class FutureDateForm(forms.Form):
    future_date = forms.DateField(initial=datetime.datetime.now(), widget=SelectDateWidget())


class ParticipantForm_add(forms.Form):
    qs = User.objects.filter(is_staff=False).filter(is_superuser=False).order_by('first_name', 'last_name', 'username')
    user_choices = [(user.pk, get_user_full_name(user)) for user in qs]
    # Fields
    user = forms.ChoiceField(choices=user_choices, label=_(u'User'))
    role = forms.ChoiceField(choices=ALLOWED_PARTICIPANT_ROLE_CHOICES, label=_(u'Role'))
