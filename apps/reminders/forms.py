import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget

from common.forms import DetailForm

from reminders.models import Reminder


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
