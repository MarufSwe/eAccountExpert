from django.contrib import admin
from .models import Shop, SalesData

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'owner_name', 'contact_number')

@admin.register(SalesData)
class SalesDataAdmin(admin.ModelAdmin):
    list_display = ('shop', 'date_uploaded')
