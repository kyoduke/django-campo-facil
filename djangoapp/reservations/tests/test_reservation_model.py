import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import time, timedelta, date, datetime 
from django.contrib.auth import get_user_model
from reservations.models import Reservation  
from football_fields.models import FootballField
from freezegun import freeze_time

User = get_user_model()

@pytest.mark.django_db
class TestReservationModel:


    @pytest.fixture
    def user(self):
        return User.objects.create_user(email='testuser@email.com', password='testpass')

    @pytest.fixture
    def football_field(self):
        return FootballField.objects.create(name='Test Field', hour_price=200)

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

    def test_reservation_upcoming_filter(self, user, football_field):
        Reservation.objects.create(
            user=user,
            football_field=football_field,
            reservation_day=date(3028, 1, 1),
            start_time=time(12,0), 
            end_time=time(13,0),
            status='finished'
        )
        Reservation.objects.create(
            user=user,
            football_field=football_field,
            reservation_day=date(3024, 9, 1),
            start_time=time(15,0), 
            end_time=time(16,0),
            status='confirmed'
        )
        Reservation.objects.create(
            user=user,
            football_field=football_field,
            reservation_day=date(3024, 10, 1),
            start_time=time(18,0), 
            end_time=time(19,0),
            status='finished'
        )
        Reservation.objects.create(
            user=user,
            football_field=football_field,
            reservation_day=date(3029, 1, 1),
            start_time=time(15,0), 
            end_time=time(16,0),
            status='confirmed'
        )

        upcoming = Reservation.objects.upcoming()
        count = upcoming.count()
        assert count == 2