from django.shortcuts import render
from django.http import HttpRequest
from reservations.forms import ReservationForm

# Create your views here.
def create_reservation(request: HttpRequest):
    form = ReservationForm()
    context = {
        'form': form,
    }
    return render(request, 'reservation/create.html', context=context)