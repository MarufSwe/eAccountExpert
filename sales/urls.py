from django.urls import path
from .views.auth_views import register, user_login
from .views.sales_views import upload_sales_data, SalesDataListView
from .views.shop_views import shop_list, shop_create

urlpatterns = [
    path('', register, name='register'),
    path('login/', user_login, name='login'),

    path('sales', SalesDataListView.as_view(), name='sales_data_list'),
    path('upload/', upload_sales_data, name='upload_sales_data'),

    path('shops/', shop_list, name='shop_list'),
    path('shops/create/', shop_create, name='shop_create'),

]
