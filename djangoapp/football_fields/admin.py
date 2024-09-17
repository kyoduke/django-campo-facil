from django.contrib import admin
from football_fields.models import FootballField, Address, Attachment
from core.admin import soft_delete


class AddressStackedInline(admin.StackedInline):
    model = Address


class AttachmentStackedInline(admin.StackedInline):
    model = Attachment


@admin.register(FootballField)
class FootBallFieldAdmin(admin.ModelAdmin):
    inlines = [AddressStackedInline, AttachmentStackedInline]
    actions = [soft_delete]


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
