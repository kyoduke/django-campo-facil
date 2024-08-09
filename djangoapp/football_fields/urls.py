from django.urls import path
from football_fields import views

urlpatterns = [
    path('new', views.football_field_list, name='create_football_field')
]
