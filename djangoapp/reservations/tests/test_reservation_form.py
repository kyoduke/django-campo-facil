import pytest
from datetime import time, date, timedelta
from reservations.forms import ReservationForm
from reservations.models import Reservation
from django.contrib.auth import get_user_model
from football_fields.models import FootballField

User = get_user_model()
@pytest.mark.django_db
class TestReservationForm:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(email='testuser@email.com', password='testpass')

    @pytest.fixture
    def football_field(self):
        return FootballField.objects.create(name='Test Field')

    @pytest.fixture
    def form_data(self):
        return {
            'reservation_day': date.today(),
            'start_time': time(14, 0),
            'end_time': time(16, 0),
        }
    
    @pytest.fixture
    def reservation_instance(self, user, football_field):
        return Reservation(user=user, football_field=football_field)

    def test_form_valid_data(self, form_data, reservation_instance):
        form = ReservationForm(data=form_data, instance=reservation_instance)
        assert form.is_valid() is True

    def test_form_missing_required_fields(self, form_data, reservation_instance):
        form_data.pop('start_time')
        form = ReservationForm(data=form_data, instance=reservation_instance)
        assert form.is_valid() is False
        assert 'start_time' in form.errors

    def test_start_time_after_end_time(self, form_data, reservation_instance):
        form_data['start_time'] = time(16, 0)
        form_data['end_time'] = time(14, 0)
        form = ReservationForm(data=form_data, instance=reservation_instance)
        assert form.is_valid() is False
        assert 'end_time' in form.errors

    def test_reservation_in_past(self, form_data, reservation_instance):
        form_data['reservation_day'] = date.today() - timedelta(days=1)
        form = ReservationForm(data=form_data, instance=reservation_instance)
        assert form.is_valid() is False
        assert 'reservation_day' in form.errors

    def test_form_save(self, user, football_field, form_data, reservation_instance):
        form = ReservationForm(data=form_data, instance=reservation_instance)
        assert form.is_valid() is True

        # Save form with user and football field manually added
        reservation = form.save(commit=False)
        reservation.save()

        # Ensure reservation was saved correctly
        assert Reservation.objects.count() == 1
        saved_reservation = Reservation.objects.first()
        assert saved_reservation.user == user
        assert saved_reservation.football_field == football_field
        assert saved_reservation.start_time == form_data['start_time']
        assert saved_reservation.end_time == form_data['end_time']
        assert saved_reservation.status == 'confirmed'
  