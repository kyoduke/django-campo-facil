import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import time, timedelta, date
from django.contrib.auth import get_user_model
from reservations.models import Reservation  
from football_fields.models import FootballField

User = get_user_model()

@pytest.mark.django_db
class TestReservationModel:


    @pytest.fixture
    def user(self):
        return User.objects.create_user(email='testuser@email.com', password='testpass')

    @pytest.fixture
    def football_field(self):
        return FootballField.objects.create(name='Test Field')

    @pytest.fixture
    def reservation(self, user, football_field):
        return Reservation.objects.create(
            user=user,
            football_field=football_field,
            reservation_day=date.today(),
            start_time=time(14, 0),
            end_time=time(16, 0),
            status='confirmed'
        )

    def test_reservation_creation(self, reservation):
        assert reservation.id is not None
        assert reservation.status == 'confirmed'
        assert reservation.__str__() == f'{reservation.football_field} | {reservation.reservation_day} | {reservation.start_time}'

    def test_start_time_after_end_time(self, user, football_field):
        with pytest.raises(ValidationError, match="End time must be after start time."):
            Reservation.objects.create(
                user=user,
                football_field=football_field,
                reservation_day=date.today(),
                start_time=time(16, 0),
                end_time=time(14, 0),
            )

    def test_reservation_in_past(self, user, football_field):
        past_date = date.today() - timedelta(days=1)
        with pytest.raises(ValidationError, match="Cannot create reservations in the past."):
            Reservation.objects.create(
                user=user,
                football_field=football_field,
                reservation_day=past_date,
                start_time=time(14, 0),
                end_time=time(16, 0),
            )

    def test_overlapping_reservations(self, user, football_field, reservation):
        with pytest.raises(ValidationError, match="This time slot overlaps with an existing reservation."):
            Reservation.objects.create(
                user=user,
                football_field=football_field,
                reservation_day=reservation.reservation_day,
                start_time=time(15, 0),
                end_time=time(17, 0),
            )

    def test_reservation_clean_method(self, reservation):
        # Modify reservation to simulate invalid state
        reservation.start_time = time(16, 0)
        reservation.end_time = time(14, 0)
        with pytest.raises(ValidationError):
            reservation.full_clean()  # This should raise a ValidationError
