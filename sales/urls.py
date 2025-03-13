from django.urls import path
from .views import upload_sales_data, SalesDataListView, shop_list, shop_create

urlpatterns = [
    path('upload/', upload_sales_data, name='upload_sales_data'),
    path('', SalesDataListView.as_view(), name='sales_data_list'),

    path('shops/', shop_list, name='shop_list'),
    path('shops/create/', shop_create, name='shop_create'),

]
