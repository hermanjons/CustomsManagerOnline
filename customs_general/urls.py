from django.urls import path

from customs_general.views.admin_views import upload_excel, upload_progress, download_failed_rows
from customs_general.views.user_views import GeneralCustomsModelListView

app_name = 'customs_general'  # Django'nun namespace içinde URL'yi bulmasını sağlıyoruz

urlpatterns = [
    path('upload-progress/', upload_progress, name='upload_progress'),
    path('upload-excel/<str:model>/', upload_excel, name="upload_excel"),
    path('download-failed-rows/<str:model>/', download_failed_rows, name='download_failed_rows'),
    path('fetch-model-detail/<str:model>/<int:pk>/', GeneralCustomsModelListView.as_view(), name='fetch_model_detail'),
    path('<str:model>/', GeneralCustomsModelListView.as_view(), name='model_data'),
]
