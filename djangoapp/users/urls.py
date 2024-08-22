from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    # path('', views.home_view),
    path('profile/', views.user_profile_view, name='profile')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
