from django.urls import reverse
from django.test import Client
from users.views import user_profile_view
import pytest
from django.contrib.messages.api import get_messages
from users.models import User


@pytest.mark.django_db
class TestUserView:

    @pytest.fixture
    def user_fixture(self):
        email = "robertjackson@gmail.com"
        password = "abc1234"
        return User.objects.create_user(email=email, password=password)

    @pytest.fixture
    def logged(self, client, user_fixture):
        return client.login(email=user_fixture.email, password="abc1234")

    def test_profile_view_authenticated(self, client, logged):
        url = reverse("profile")
        response = client.get(url)

        assert response.status_code == 200
        assert logged is True

    def test_profile_view_unauthenticated(self, client):
        url = reverse("profile")
        response = client.get(url)
        assert response.status_code == 302
