import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from football_fields.models import FootballField, Address
from reservations.models import Reservation
from datetime import timedelta, time

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(email="testuser@test.com", password="12345")


@pytest.fixture
def football_field(user):
    field = FootballField.objects.create(
        owner=user,
        name="Test Field",
        main_image="test.jpg",
        field_dimensions="100x50",
        description="A test football field",
        grass_type="SIN",
        has_field_lighting=True,
        has_changing_room=True,
        hour_price=100,
        facilities="Parking available",
        rules="No smoking",
    )
    Address.objects.create(
        football_field=field,
        address_one="123 Test St",
        state="SP",
        city="São Paulo",
        district="Test District",
        cep_code="12345-678",
    )
    return field


@pytest.fixture
def reservation(user, football_field):
    return Reservation.objects.create(
        user=user,
        football_field=football_field,
        reservation_day=timezone.now().date() + timedelta(days=1),
        start_time=time(10, 0),
        end_time=time(11, 0),
        total_cost=100,
    )
