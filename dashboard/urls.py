from django.urls import path, include
from .views import dashboard_home

urlpatterns = [
    path('', dashboard_home, name='dashboard_home'),
    path('customs-general/', include('customs_general.urls', namespace='customs_general')),  # Custom General URL'leri buraya bağladık!
]

