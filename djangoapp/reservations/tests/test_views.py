import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from football_fields.models import FootballField
from django.http import HttpResponse
from django.test import Client
from datetime import datetime, timedelta
from reservations.models import Reservation

User = get_user_model()


class TestReservationViews:

    @pytest.fixture
    def logged_user(self, db, user, client: Client):
        return client.login(email=user.email, password="testpass")

    def test_unauthenticaded_access(self, client):
        url = reverse("create_reservation", args=[17])
        response = client.get(url)
        assert response.status_code == 302
        assert "/accounts/login" in response.url

    def test_authenticated_access(self, db, football_field, user, client: Client):
        logged = client.login(email=user.email, password="testpass")
        url = reverse("create_reservation", args=[football_field.pk])
        response: HttpResponse = client.get(url)

        assert response.status_code == 200
        assert logged is True

    def test_form_rendered(self, db, user, football_field, client: Client, logged_user):
        """
        Tests if the form is being rendered with all input fields.
        """
        url = reverse("create_reservation", args=[football_field.pk])
        response: HttpResponse = client.get(url)
        html_content = response.content.decode("utf-8")

        assert "form" in response.context
        assert '<input type="date" name="reservation_day"' in html_content
        assert '<input type="time" name="start_time"' in html_content
        assert '<input type="time" name="end_time"' in html_content

    def test_reservation_creation_via_post(
        self, db, user, football_field, client: Client, logged_user
    ):
        url = reverse("create_reservation", args=[football_field.pk])
        data = {
            "reservation_day": datetime.now().date(),
            "start_time": (datetime.now() + timedelta(hours=1))
            .time()
            .strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=2)).time().strftime("%H:%M"),
        }
        response: HttpResponse = client.post(url, data=data)
        count = Reservation.objects.all().count()

        assert count == 1

    def test_handle_nonexistent_football_field(self, logged_user, client: Client):
        """
        Asserts the user is being redirected when there is no football field associated with given url arg
        """
        url = reverse("create_reservation", args=[199])
        response: HttpResponse = client.get(url)

        assert response.status_code == 302
        assert response.url == "/"

    def test_form_errors(self, logged_user, football_field, client: Client):
        """ """
        url = reverse("create_reservation", args=[football_field.pk])
        data = {
            "reservation_day": datetime.now().date(),
            "start_time": (datetime.now() + timedelta(hours=-1))
            .time()
            .strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=2)).time().strftime("%H:%M"),
        }
        response: HttpResponse = client.post(url, data=data)
        print(data)
        assert response.status_code == 200
        assert "errorlist" in response.content.decode("utf-8")
