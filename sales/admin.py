from django.contrib import admin
from .models import Shop, SalesData, SlicerList, CatListD, CatListC

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'owner_name', 'contact_number')

@admin.register(SalesData)
class SalesDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'date_uploaded')


admin.site.register(SlicerList)
admin.site.register(CatListD)
admin.site.register(CatListC)
