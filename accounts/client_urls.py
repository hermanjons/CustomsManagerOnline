from django.urls import path, include

urlpatterns = [
    path('products/', include(('products.urls', 'products'))),
    path('dashboard/', include(('dashboard.urls', 'client_dashboard'))),
]
