from django.contrib import admin
from .models import Reservation

# Register your models here.
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass
