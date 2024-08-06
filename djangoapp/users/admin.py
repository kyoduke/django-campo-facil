from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.



class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",  
        "profile_image",  
        "phone_number",  
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "profile_image",  
        "phone_number",
    )
    fieldsets = (
        (None, {"fields": (
            "first_name",
            "last_name", 
            "email", 
            "password", 
            "profile_image",  
            "phone_number",  
            )}
        ),
        ("Permissions", {"fields": (
            "is_staff", 
            "is_active", 
            "groups", 
            "user_permissions")}
        ),
    )
    add_fieldsets = (
        ( None, {"fields": (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions")}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)



admin.site.register(User, CustomUserAdmin)