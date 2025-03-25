from django.urls import path

from .views import model_data, upload_excel
app_name = 'customs_general'  # Django'nun namespace içinde URL'yi bulmasını sağlıyoruz

urlpatterns = [
    path('<str:model>/', model_data, name='model_data'),
    path('upload-excel/<str:model>/', upload_excel, name="upload_excel"),

]
