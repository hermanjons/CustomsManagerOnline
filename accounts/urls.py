from django.urls import path
from .views import login_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('giris/', login_view, name='login'),
    path('cikis/', LogoutView.as_view(next_page='login'), name='logout'),
]
