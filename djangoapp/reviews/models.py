from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
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

    rating = models.PositiveSmallIntegerField(default=1, choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)


    def clean(self):
        # can't create two reviews for the same football field
        if Review.objects.filter(football_field=self.football_field, author=self.author, is_active=True).exclude(pk=self.pk).exists() > 0:
            raise ValidationError(_('You have already submitted a review for this football field.'))


    def soft_delete(self):
        """
        Changes the active status of the object to False.
        """
        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)