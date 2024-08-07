import pytest
from users.models import User
from django.db import models
from django.contrib.auth import get_user_model


def test_issubclass():
    assert issubclass(User, models.Model)


@pytest.mark.django_db
def test_has_aall_attributes(user_factory):
    user: User = user_factory() 
    assert hasattr(user, 'first_name')
    assert hasattr(user, 'last_name')
    assert hasattr(user, 'email')
    assert hasattr(user, 'password')
    assert hasattr(user, 'phone_number')
    assert hasattr(user, 'profile_image')
