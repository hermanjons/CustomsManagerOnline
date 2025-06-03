from django.urls import path, include

urlpatterns = [
    path('customs_general/', include(('customs_general.urls', 'customs_general'))),
    path('dashboard/', include(('dashboard.urls', 'consultant_dashboard'))),
]
