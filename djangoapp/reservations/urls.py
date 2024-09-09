from django.urls import path
from reservations import views

urlpatterns = [
    path("<int:pk>/create/", views.create_reservation, name="create_reservation"),
    path("<int:pk>/detail/", views.detail_reservation, name="detail_reservation"),
    path("<int:pk>/cancel/", views.cancel_reservation, name="cancel_reservation"),
    path("", views.user_reservations, name="user_reservations"),
]
