from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Reservation, BlockedTimeSlot

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ('user','football_field', 'status', 'total_cost')

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)

    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    
    def save(self, commit=True):
        instance = super(ReservationForm, self).save(commit=False)


        if commit:
            instance.save()
        
        return instance