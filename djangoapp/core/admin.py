from django.contrib import admin
from django.utils.translation import gettext as _


@admin.action(description=_("Mark selected as inactive"))
def soft_delete(modeladmin, request, queryset):
    for obj in queryset:
        obj.soft_delete()
