from django.urls import path

from sales.views.reconciliation.reconcile_sales_data_views import reconcile_sales_data
from sales.views.reconciliation.reconciliation_list_views import reconciliation_list

from .views.auth_views import register, user_login, user_logout
from .views.sales_views import upload_sales_data, SalesDataListView
from .views.shop_views import shop_list, shop_create

from sales.views.reconciliation.slicer_list_views import *
from sales.views.reconciliation.cat_list_c_views import *
from sales.views.reconciliation.cat_list_d_views import *

urlpatterns = [
    path('', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),


    path('sales', SalesDataListView.as_view(), name='sales_data_list'),
    path('upload/', upload_sales_data, name='upload_sales_data'),

    path('shops/', shop_list, name='shop_list'),
    path('shops/create/', shop_create, name='shop_create'),

    # SlicerList
    path('slicer/', SlicerListView.as_view(), name='slicer_list'),
    path('slicer/add/', SlicerCreateView.as_view(), name='slicer_add'),
    path('slicer/edit/<int:pk>/', SlicerUpdateView.as_view(), name='slicer_edit'),
    path('slicer/delete/<int:pk>/', SlicerDeleteView.as_view(), name='slicer_delete'),

    # CatListD
    path('catlistd/', CatListDView.as_view(), name='catlistd_list'),
    path('catlistd/add/', CatListDCreateView.as_view(), name='catlistd_add'),
    path('catlistd/edit/<int:pk>/', CatListDUpdateView.as_view(), name='catlistd_edit'),
    path('catlistd/delete/<int:pk>/', CatListDDeleteView.as_view(), name='catlistd_delete'),

    # CatListC
    path('catlistc/', CatListCView.as_view(), name='catlistc_list'),
    path('catlistc/add/', CatListCCreateView.as_view(), name='catlistc_add'),
    path('catlistc/edit/<int:pk>/', CatListCUpdateView.as_view(), name='catlistc_edit'),
    path('catlistc/delete/<int:pk>/', CatListCDeleteView.as_view(), name='catlistc_delete'),

    # path('import/', import_bank_statement, name='import_bank_statement'),
    path("reconcile/<int:sales_data_id>/", reconcile_sales_data, name="reconcile_sales_data"),

    path('sales_data/<int:sales_data_id>/reconciliation/', reconciliation_list, name='reconciliation_list'),




]
