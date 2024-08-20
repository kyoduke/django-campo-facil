from django.db import models
from django.contrib.auth import get_user_model
from football_fields.models import FootballField
from django.core.exceptions import ValidationError
import datetime 
from django.utils.translation import gettext as _
# Create your models here.

User = get_user_model()

class ReservationManager(models.Manager):
    def upcoming(self):
        return self.filter(status='confirmed')
    


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('finished', 'Finished'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    football_field = models.ForeignKey(FootballField, on_delete=models.CASCADE, related_name='reservations')
    reservation_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReservationManager()

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f'{self.football_field} | {self.reservation_day} | {self.start_time}'

    def clean(self):
        if isinstance(self.start_time, datetime.time) and isinstance(self.end_time, datetime.time) and isinstance(self.reservation_day, datetime.date):
            if self.start_time >= self.end_time:
                raise ValidationError({'end_time':_('End time must be after start time.')}) 
            
            if self.reservation_day < datetime.datetime.now().date():
                raise ValidationError({'reservation_day':_('Cannot create reservations in the past.')})

            # Check if the reservation date being saved conflicts
            # with other reservation date
            overlapping = Reservation.objects.filter(
                football_field=self.football_field, 
                reservation_day=self.reservation_day,
                start_time__lt=self.end_time, 
                end_time__gt=self.start_time     
            ).exclude(pk=self.pk)

            if overlapping.exists():
                raise ValidationError(_('This time slot overlaps with an existing reservation.'))


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)