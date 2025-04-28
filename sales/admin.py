from django.contrib import admin
from .models import Reconciliation, Shop, SalesData, CategoryMapping

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'owner_name', 'contact_number')

@admin.register(SalesData)
class SalesDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'date_uploaded')


@admin.register(CategoryMapping)
class CategoryMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'slicer_list', 'cat_list_d', 'cat_list_c')
    

@admin.register(Reconciliation)
class ReconciliationAdmin(admin.ModelAdmin):
    list_display = ('id', "sales_data", "description", "amount", "credit_amount", "debit_amount", "slicer_new", "category_new")
    search_fields = ("amount",)
    list_filter = ("credit_amount", "debit_amount")

    def get_queryset(self, request):
        """Ensure the admin panel only loads necessary fields to improve performance."""
        return super().get_queryset(request).only("description", "amount", "credit_amount", "debit_amount")

