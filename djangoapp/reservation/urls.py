from django.urls import path
from reservation import views

urlpatterns = [
    path('new', views.create_reservation, name='new_reservation'),
]

