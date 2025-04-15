from django.urls import path

from .views import upload_excel, upload_progress, download_failed_rows, fetch_model_detail, GeneralCustomsModelListView
app_name = 'customs_general'  # Django'nun namespace içinde URL'yi bulmasını sağlıyoruz

urlpatterns = [
    path('<str:model>/', GeneralCustomsModelListView.as_view(), name='model_data'),
    path('upload-excel/<str:model>/', upload_excel, name="upload_excel"),
    path('upload-progress/', upload_progress, name='upload_progress'),
    path('download-failed-rows/<str:model>/', download_failed_rows, name='download_failed_rows'),
    path('/customs_general/fetch-model-detail/<str:model_name>/<int:pk>/', fetch_model_detail, name='fetch_model_detail'),

]
