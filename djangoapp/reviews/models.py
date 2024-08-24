from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from football_fields.models import FootballField
from reservations.models import Reservation

User = get_user_model()

class Review(models.Model):

    RATING_CHOICES = [
        (1, _('1 Star')),
        (2, _('2 Stars')),
        (3, _('3 Stars')),
        (4, _('4 Stars')),
        (5, _('5 Stars')),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    football_field = models.ForeignKey(FootballField, on_delete=models.CASCADE, related_name='reviews')
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='review')

    rating = models.PositiveSmallIntegerField(default=1, choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def soft_delete(self):
        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)