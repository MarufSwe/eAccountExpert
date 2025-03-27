# for dynamic csv columns
from django.db import models
from django.db.models import JSONField

class Shop(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class SalesData(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    data = JSONField(null=True, blank=True)  # This will store the entire row as a dictionary (dynamic)

    def __str__(self):
        return f"Sales data for {self.shop.name} uploaded on {self.date_uploaded}"

    class Meta:
        db_table = "sales_data"


# For Reconcilation
class SlicerList(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class CatListD(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class CatListC(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name