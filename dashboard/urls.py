from django.urls import path

from .views import dashboard_home, model_data

urlpatterns = [
    path('', dashboard_home, name='dashboard_home'),
    path('model-data/<str:model>/', model_data, name='model_data'),

]
