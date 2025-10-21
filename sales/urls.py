from django.urls import path

from sales.views.reconciliation.category_mapping_views import *
from sales.views.reconciliation.reconcile_sales_data_views import reconcile_sales_data
from sales.views.reconciliation.reconciliation_list_views import reconciliation_list, update_reconciliation_field
from sales.views.reconciliation.pl_report_views import pl_report, pl_report_json
from sales.views.reconciliation.reconciliation_stats_views import reconciliation_stats, reconciliation_stats_json

from .views.auth_views import register, user_login, user_logout
from .views.sales_views import upload_sales_data, SalesDataListView
from .views.shop_views import shop_list, shop_create, shop_selection, select_shop


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # Shop selection (landing after login)
    path('select-shop/', shop_selection, name='shop_selection'),
    path('select-shop/submit/', select_shop, name='select_shop'),

    # Sales data (requires shop selection)
    path('sales', SalesDataListView.as_view(), name='sales_data_list'),
    path('upload/', upload_sales_data, name='upload_sales_data'),

    # Shop management
    path('shops/', shop_list, name='shop_list'),
    path('shops/create/', shop_create, name='shop_create'),

    # CategoryMapping
    path('category-mapping/', category_mapping_list, name='category_mapping_list'),
    path('category-mapping/add/', category_mapping_create, name='category_mapping_create'),
    path('category-mapping/edit/<int:pk>/', category_mapping_update, name='category_mapping_update'),
    path('category-mapping/delete/<int:pk>/', category_mapping_delete, name='category_mapping_delete'),

    # Reconcile button for SalseData 
    path("reconcile/<int:sales_data_id>/", reconcile_sales_data, name="reconcile_sales_data"),
    # Reconciled data list
    path('sales_data/<int:sales_data_id>/reconciliation/', reconciliation_list, name='reconciliation_list'),
    # Update reconciliation fields
    path('reconciliation/<int:reconciliation_id>/update/', update_reconciliation_field, name='update_reconciliation_field'),
    # P&L Report
    path('sales_data/<int:sales_data_id>/pl-report/', pl_report, name='pl_report'),
    path('sales_data/<int:sales_data_id>/pl-report/json/', pl_report_json, name='pl_report_json'),
    # Reconciliation Statistics
    path('sales_data/<int:sales_data_id>/stats/', reconciliation_stats, name='reconciliation_stats'),
    path('sales_data/<int:sales_data_id>/stats/json/', reconciliation_stats_json, name='reconciliation_stats_json'),

]
