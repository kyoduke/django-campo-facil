from django.contrib import admin
from football_fields.models import FootballField, Address, Attachment

# Register your models here.


class AddressStackedInline(admin.StackedInline):
    model = Address


class AttachmentStackedInline(admin.StackedInline):
    model = Attachment


@admin.register(FootballField)
class FootBallFieldAdmin(admin.ModelAdmin):
    inlines = [AddressStackedInline, AttachmentStackedInline]


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
