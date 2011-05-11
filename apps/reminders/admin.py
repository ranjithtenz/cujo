from django.contrib import admin

from reminders.models import Reminder, Participant

class ParticipantInline(admin.StackedInline):
    model = Participant
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class ReminderAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline]


admin.site.register(Reminder, ReminderAdmin)
