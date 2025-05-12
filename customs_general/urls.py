from django.urls import path
from .views import upload_excel, upload_progress, download_failed_rows,GeneralCustomsModelListView


app_name = 'customs_general'  # Django'nun namespace içinde URL'yi bulmasını sağlıyoruz

urlpatterns = [
    path('<str:model>/', GeneralCustomsModelListView.as_view(), name='model_data'),
    path('upload-excel/<str:model>/', upload_excel, name="upload_excel"),
    path('upload-progress/', upload_progress, name='upload_progress'),
    path('download-failed-rows/<str:model>/', download_failed_rows, name='download_failed_rows'),
    path('fetch-model-detail/<str:model>/<int:pk>/', GeneralCustomsModelListView.as_view(), name='fetch_model_detail'),

]
