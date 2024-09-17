import pytest
from django.db import models
from users.models import User


@pytest.mark.django_db
class TestUserModel:

    def test_issubclass(self):
        assert issubclass(User, models.Model)

    def test_has_aall_attributes(self, user_factory):
        user = user_factory()
        assert hasattr(user, "first_name")
        assert hasattr(user, "last_name")
        assert hasattr(user, "email")
        assert hasattr(user, "password")
        assert hasattr(user, "phone_number")
        assert hasattr(user, "profile_image")

    def test_user_creation_without_email_(self):
        with pytest.raises(
            ValueError, match="You have not provided a valid e-mail address."
        ):
            user = User.objects.create_user(email="", password="abc123")

    def test_if_superuser_has_superuser_attributes(self):
        superuser = User.objects.create_superuser(
            email="test@test.com", password="test@1234"
        )
        assert superuser.is_staff is True
        assert superuser.is_superuser is True

    def test_get_short_name_method(self):
        user_1 = User.objects.create_user(
            first_name="Testing", email="test@test.com", password="abc123"
        )
        user_2 = User.objects.create_user(
            email="shortnametest@test.com", password="abc123"
        )
        assert user_1.get_short_name() == user_1.first_name
        assert user_2.get_short_name() == user_2.email.split("@")[0]
