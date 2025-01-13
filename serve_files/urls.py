from django.urls import path
from .views import *
from django.conf import settings

app_name = 'serve_files'
if not hasattr(settings, 'SERVE_DECRYPTED_FILE_URL_BASE'):
    raise ValueError("SERVE_DECRYPTED_FILE_URL_BASE must be set in your environment.")
base_url_serve_decrypted_file = settings.SERVE_DECRYPTED_FILE_URL_BASE

urlpatterns = [
  path(f'{base_url_serve_decrypted_file}/<str:app_name>/<str:model_name>/<str:field_name>/<int:pk>/', serve_decrypted_file, name='serve_decrypted_file'),
]
