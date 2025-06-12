from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import select_active_consultant, login_view, select_active_client
urlpatterns = [
    path('giris/', login_view, name='login'),
    path('cikis/', LogoutView.as_view(next_page='login'), name='logout'),
    path("select-client/<int:client_id>/", select_active_client, name="select_active_client"),
    path('select_active_consultant/<int:consultant_id>/', select_active_consultant, name='select_active_consultant'),

]
