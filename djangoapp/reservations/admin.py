from django.contrib import admin
from .models import Reservation, BlockedTimeSlot

# Register your models here.
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass

@admin.register(BlockedTimeSlot)
class BlockedTimeSlotAdmin(admin.ModelAdmin):
    pass