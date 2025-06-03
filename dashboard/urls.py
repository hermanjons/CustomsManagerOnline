from django.urls import path, include
from .views import DashboardHomeView

urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard_home'),
]
