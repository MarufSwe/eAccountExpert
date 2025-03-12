from django.urls import path
from .views import upload_sales_data

urlpatterns = [
    path('upload/', upload_sales_data, name='upload_sales_data'),
]
