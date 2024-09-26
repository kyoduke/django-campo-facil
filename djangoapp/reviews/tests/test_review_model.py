import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from football_fields.models import FootballField
from reservations.models import Reservation
from reviews.models import Review

User = get_user_model()


@pytest.fixture
def review(user, football_field):
    return Review.objects.create(
        author=user, football_field=football_field, rating=4, comment="Great field!"
    )


@pytest.mark.django_db
class TestReviewModel:

    def test_review_creation(self, review):
        assert isinstance(review, Review)
        assert str(review.author) == "testuser@test.com"
        assert str(review.football_field) == "Test Field"
        assert review.rating == 4
        assert review.comment == "Great field!"
        assert review.is_active == True

    def test_review_rating_choices(self, football_field):
        for rating in range(1, 6):
            user = User.objects.create_user(f"user{rating}@test.com", "password123")
            review = Review.objects.create(
                author=user,
                football_field=football_field,
                rating=rating,
                comment=f"{rating} star review",
            )
            assert review.rating in dict(Review.RATING_CHOICES)

    def test_invalid_rating(self, user, football_field):
        with pytest.raises(ValidationError):
            Review.objects.create(
                author=user,
                football_field=football_field,
                rating=6,
                comment="Invalid rating",
            )

    def test_duplicate_review(self, review, user, football_field):
        with pytest.raises(ValidationError):
            Review.objects.create(
                author=user,
                football_field=football_field,
                rating=3,
                comment="Duplicate review",
            )

    def test_soft_delete(self, review):
        assert review.is_active == True
        review.soft_delete()
        assert review.is_active == False

    def test_create_review_after_soft_delete(self, user, football_field):
        review1 = Review.objects.create(
            author=user, football_field=football_field, rating=4, comment="First review"
        )
        review1.soft_delete()

        review2 = Review.objects.create(
            author=user,
            football_field=football_field,
            rating=3,
            comment="Second review",
        )
        assert (
            Review.objects.filter(
                author=user, football_field=football_field, is_active=True
            ).count()
            == 1
        )

    def test_review_timestamps(self, review):
        assert review.created_at is not None
        assert review.updated_at is not None
        assert isinstance(review.created_at, timezone.datetime)
        assert isinstance(review.updated_at, timezone.datetime)

    def test_review_update(self, review):
        original_updated_at = review.updated_at
        review.rating = 5
        review.comment = "Updated comment"
        review.save()
        review.refresh_from_db()
        assert review.rating == 5
        assert review.comment == "Updated comment"
        assert review.updated_at > original_updated_at

    def test_review_related_names(self, user, football_field, review):
        assert review in user.reviews.all()
        assert review in football_field.reviews.all()

    def test_cascade_delete_user(self, user, football_field, review):
        user.delete()
        with pytest.raises(Review.DoesNotExist):
            review.refresh_from_db()

    def test_cascade_delete_football_field(self, user, football_field, review):
        football_field.delete()
        with pytest.raises(Review.DoesNotExist):
            review.refresh_from_db()

    def test_review_after_reservation(self, user, football_field, reservation):
        review = Review.objects.create(
            author=user,
            football_field=football_field,
            rating=5,
            comment="Excellent field, had a great time!",
        )
        assert review.football_field == reservation.football_field

    def test_multiple_reviews_different_fields(self, user):
        field1 = FootballField.objects.create(
            owner=user, name="Field 1", hour_price=100, main_image="test.jpg"
        )
        field2 = FootballField.objects.create(
            owner=user, name="Field 2", hour_price=120, main_image="test.jpg"
        )

        Review.objects.create(
            author=user, football_field=field1, rating=4, comment="Good field"
        )
        Review.objects.create(
            author=user, football_field=field2, rating=5, comment="Great field"
        )

        assert Review.objects.filter(author=user).count() == 2

    def test_review_with_football_field_details(self, user, football_field):
        review = Review.objects.create(
            author=user,
            football_field=football_field,
            rating=4,
            comment="Good field with nice facilities",
        )
        assert review.football_field.name == "Test Field"
        assert review.football_field.grass_type == "SIN"
        assert review.football_field.has_field_lighting == True
        assert review.football_field.has_changing_room == True

    def test_review_with_address(self, user, football_field):
        review = Review.objects.create(
            author=user,
            football_field=football_field,
            rating=5,
            comment="Excellent location",
        )
        assert review.football_field.address.city == "São Paulo"
        assert review.football_field.address.state == "SP"

    def test_review_count_for_football_field(self, user, football_field):
        Review.objects.create(
            author=user, football_field=football_field, rating=4, comment="Good"
        )
        Review.objects.create(
            author=User.objects.create_user("user2@test.com", "password123"),
            football_field=football_field,
            rating=5,
            comment="Excellent",
        )

        assert football_field.reviews.count() == 2

    def test_average_rating_for_football_field(self, user, football_field):
        Review.objects.create(
            author=user, football_field=football_field, rating=4, comment="Good"
        )
        Review.objects.create(
            author=User.objects.create_user("user2@test.com", "password123"),
            football_field=football_field,
            rating=5,
            comment="Excellent",
        )

        avg_rating = football_field.reviews.aggregate(models.Avg("rating"))[
            "rating__avg"
        ]
        assert avg_rating == 4.5

    def test_review_without_reservation(self, user, football_field):
        review = Review.objects.create(
            author=user,
            football_field=football_field,
            rating=3,
            comment="Average field, but I have not played here yet",
        )
        assert review.football_field == football_field
        assert not Reservation.objects.filter(
            user=user, football_field=football_field
        ).exists()
