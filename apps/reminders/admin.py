from django.contrib import admin

from reminders.models import Reminder

#class PermissionHolderInline(admin.StackedInline):
#    model = PermissionHolder
#    extra = 1
#    classes = ('collapse-open',)
#    allow_add = True


#class PermissionAdmin(admin.ModelAdmin):
#    inlines = [PermissionHolderInline]
#    list_display = ('namespace', 'name', 'label')
#    list_display_links = list_display

admin.site.register(Reminder)
