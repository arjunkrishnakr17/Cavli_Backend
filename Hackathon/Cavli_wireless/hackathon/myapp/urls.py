from django.urls import path
from .views import upload_file, get_file_info

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('get_file/<int:file_id>/', get_file_info, name='get_file_info'),
]
