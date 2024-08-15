from django.urls import path
from reservations import views

urlpatterns = [
    path('new', views.create_reservation, name='new_reservation'),
]

