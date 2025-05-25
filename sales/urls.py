from django.urls import path

from sales.views.reconciliation.category_mapping_views import *
from sales.views.reconciliation.reconcile_sales_data_views import reconcile_sales_data
from sales.views.reconciliation.reconciliation_list_views import reconciliation_list

from .views.auth_views import register, user_login, user_logout
from .views.sales_views import upload_sales_data, SalesDataListView
from .views.shop_views import shop_list, shop_create


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),


    path('sales', SalesDataListView.as_view(), name='sales_data_list'),
    path('upload/', upload_sales_data, name='upload_sales_data'),

    path('shops/', shop_list, name='shop_list'),
    path('shops/create/', shop_create, name='shop_create'),

    # CategoryMapping
    path('category-mapping/', category_mapping_list, name='category_mapping_list'),
    path('category-mapping/add/', category_mapping_create, name='category_mapping_create'),
    path('category-mapping/edit/<int:pk>/', category_mapping_update, name='category_mapping_update'),
    path('category-mapping/delete/<int:pk>/', category_mapping_delete, name='category_mapping_delete'),

    # path('import/', import_bank_statement, name='import_bank_statement'),
    path("reconcile/<int:sales_data_id>/", reconcile_sales_data, name="reconcile_sales_data"),

    path('sales_data/<int:sales_data_id>/reconciliation/', reconciliation_list, name='reconciliation_list'),

]
