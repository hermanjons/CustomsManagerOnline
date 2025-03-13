from django.urls import path, include
from .views import dashboard_home

urlpatterns = [
    path('', dashboard_home, name='dashboard_home'),
            ]

