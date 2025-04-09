from django.contrib import admin
from .models import Reconciliation, Shop, SalesData, SlicerList, CatListD, CatListC

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'owner_name', 'contact_number')

@admin.register(SalesData)
class SalesDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'date_uploaded')


class SlicerListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Display ID and name
    search_fields = ('name',)  # Add search by name
    list_filter = ('name',)  # Add filter by name

class CatListDAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)

class CatListCAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)

admin.site.register(SlicerList, SlicerListAdmin)
admin.site.register(CatListD, CatListDAdmin)
admin.site.register(CatListC, CatListCAdmin)


# @admin.register(ReconciliationData)
# class ReconciliationDataAdmin(admin.ModelAdmin):
#     list_display = ('description', 'amount', 'credit_amount', 'debit_amount')  # Fields to show in the list view
#     search_fields = ('amount',)  # Make description searchable
#     list_filter = ('credit_amount', 'debit_amount')  # Add filter options for credit and debit amounts
#     ordering = ('-id',)  # Order by most recent first


@admin.register(Reconciliation)
class ReconciliationAdmin(admin.ModelAdmin):
    list_display = ('id', "sales_data", "description", "amount", "credit_amount", "debit_amount", "slicer_new", "category_new")
    search_fields = ("amount",)
    list_filter = ("credit_amount", "debit_amount")

    def get_queryset(self, request):
        """Ensure the admin panel only loads necessary fields to improve performance."""
        return super().get_queryset(request).only("description", "amount", "credit_amount", "debit_amount")

