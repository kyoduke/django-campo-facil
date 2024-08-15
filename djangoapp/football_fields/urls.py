from django.urls import path
from football_fields import views

urlpatterns = [
    path('', views.football_field_list, name='football_field_list'),
    path('<int:pk>', views.football_field_detail, name='football_field_detail'),
    path('new', views.create_football_field, name='create_football_field'),
]
