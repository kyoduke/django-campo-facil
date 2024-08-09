from django.urls import path
from football_fields import views

urlpatterns = [
    path('new', views.create_football_field, name='create_football_field'),
]
