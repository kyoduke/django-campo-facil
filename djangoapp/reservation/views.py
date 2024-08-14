from django.shortcuts import render
from django.http import HttpRequest
# Create your views here.
def create_reservation(request: HttpRequest):
    return render(request, 'reservation/create.html')