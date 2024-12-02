from django.urls import path
from .views import upload_pdf
from .views import index, download_report
from .views import home


urlpatterns = [
    path('upload/', upload_pdf, name='upload_pdf'),
    path('', index, name='upload.html'),
    # path('', home, name='home'),
    path('download_report/', download_report, name='download_report'),
]
