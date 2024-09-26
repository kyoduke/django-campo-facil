import pytest
from football_fields.models import FootballField
from django.contrib.auth import get_user_model
from reservations.models import Reservation
from datetime import datetime, timedelta, time

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(email="testuser@email.com", password="testpass")


@pytest.fixture
def football_field(user):
    return FootballField.objects.create(
        owner=user, name="Test Field", hour_price=200, main_image="test.jpg"
    )


@pytest.fixture
def reservation(user, football_field):
    return Reservation.objects.create(
        user=user,
        football_field=football_field,
        reservation_day=(datetime.now() + timedelta(days=1)).date(),
        start_time=time(14, 0),
        end_time=time(16, 0),
        status="confirmed",
        total_cost=250,
    )
