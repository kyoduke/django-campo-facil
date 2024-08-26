from django.urls import path 
from reviews import views

urlpatterns = [
    path('<int:pk>', views.create_review, name='create_review')
]
