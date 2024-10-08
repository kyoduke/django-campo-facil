from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(
        verbose_name="nome", max_length=100, blank=True, default=""
    )
    last_name = models.CharField(
        verbose_name="sobrenome", max_length=100, blank=True, default=""
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    profile_image = models.ImageField(
        null=True, blank=True, upload_to="users_profile_image"
    )
    phone_number = PhoneNumberField(blank=True)

    objects: CustomUserManager = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name or self.email.split("@")[0]
