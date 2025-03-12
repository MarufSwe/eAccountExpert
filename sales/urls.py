from django.urls import path
from .views import upload_sales_data, SalesDataListView

urlpatterns = [
    path('upload/', upload_sales_data, name='upload_sales_data'),
    path('sales-list/', SalesDataListView.as_view(), name='sales_data_list'),

]
