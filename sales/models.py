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
    

class ReconciliationData(models.Model):
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    credit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    debit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Automatically assign Credit or Debit Amount based on Amount
        if self.amount > 0:
            self.credit_amount = self.amount
            self.debit_amount = 0
        else:
            self.debit_amount = abs(self.amount)
            self.credit_amount = 0

        super().save(*args, **kwargs)
