from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.db.models import Q
from football_fields.models import FootballField
import datetime 
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
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
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

            # only runs if the object is being created
            if self.pk is None:
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

            # Check if the time is blocked
            blocked_slots = BlockedTimeSlot.objects.filter(
                football_field=self.football_field,
                block_day=self.reservation_day,
                is_active=True
            ).filter(
                Q(start_time__lt=self.end_time) & Q(end_time__gt=self.start_time)
            )

            if blocked_slots.exists():
                raise ValidationError(_('This date and time is currently blocked.'))


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



class BlockedTimeSlot(models.Model):
    football_field = models.ForeignKey(FootballField, on_delete=models.CASCADE, related_name='blocked_slots')
    block_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def soft_delete(self):
        self.is_active = False

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)