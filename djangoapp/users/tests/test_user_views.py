from users.views import user_profile_view
import pytest
from users.models import User

@pytest.mark.django_db
def test_profile_view_authenticated(client):
    email = 'robertjackson@gmail.com'
    password = 'abc1234'
    User.objects.create_user(email=email, password=password)
    logged = client.login(email=email, password=password)
    response = client.get('/')
    assert response.status_code == 200


def test_profile_view_unauthenticated(client):
    response = client.get('/')
    assert response.status_code == 302