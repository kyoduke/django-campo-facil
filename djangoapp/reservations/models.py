from django.db import models
from django.contrib.auth import get_user_model
from football_fields.models import FootballField
from datetime import timedelta, datetime
from django.core.exceptions import ValidationError
# Create your models here.

User = get_user_model()

class ReservationManager(models.Manager):
    def upcoming(self):
        return self.filter(start_time__gt=datetime.now())
    


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    football_field = models.ForeignKey(FootballField, on_delete=models.CASCADE, related_name='reservations')
    reservation_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReservationManager()

    class Meta:
        ordering = ['-start_time']

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError('End time must be after start time.') 
        
        if self.start_time < datetime.now().time():
            print(self.start_time)
            print(datetime.now())
            raise ValidationError('Cannot create reservations in the past.')

        # Check if the reservation date being saved conflicts
        # with other reservation date
        overlapping = Reservation.objects.filter(
            football_field=self.football_field, 
            start_time__lt=self.end_time, 
            end_time__gt=self.start_time     
        ).exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError('This time slot overlaps with an existing reservation.')


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)