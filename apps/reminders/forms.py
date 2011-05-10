from django import forms
from django.utils.translation import ugettext_lazy as _

from common.forms import DetailForm

from reminders.models import Reminder


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder


class ReminderForm_view(DetailForm):
    class Meta:
        model = Reminder
