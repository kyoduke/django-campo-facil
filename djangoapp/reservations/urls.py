from django.urls import path
from reservations import views

urlpatterns = [
    path('<int:pk>', views.create_reservation, name='new_reservation'),
    path('reservations', views.user_reservations, name='user_reservations')
]

