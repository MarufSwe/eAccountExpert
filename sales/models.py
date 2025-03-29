# for dynamic csv columns
from decimal import Decimal
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

    def is_reconciled(self):
        return self.reconciliation_set.exists() 
    
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
    

# class ReconciliationData(models.Model):
#     description = models.TextField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

#     credit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     debit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def save(self, *args, **kwargs):
#         # Automatically assign Credit or Debit Amount based on Amount
#         if self.amount > 0:
#             self.credit_amount = self.amount
#             self.debit_amount = 0
#         else:
#             self.debit_amount = abs(self.amount)
#             self.credit_amount = 0

#         super().save(*args, **kwargs)


class Reconciliation(models.Model):
    description = models.TextField()  # Description field
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount field
    slicer_new = models.TextField(blank=True, null=True)  # Placeholder for future logic
    category_new = models.TextField(blank=True, null=True)  # Placeholder for future logic
    credit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    debit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # ForeignKey relationships to your Slicer_List, Cat_List_d, and Cat_List_c
    slicer_list = models.ForeignKey(SlicerList, on_delete=models.SET_NULL, null=True, blank=True)
    cat_list_d = models.ForeignKey(CatListD, on_delete=models.SET_NULL, null=True, blank=True)
    cat_list_c = models.ForeignKey(CatListC, on_delete=models.SET_NULL, null=True, blank=True)

    # ForeignKey to link Reconciliation to the SalesData entry
    sales_data = models.ForeignKey(SalesData, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Automatically assign Credit or Debit Amount based on Amount
        if self.amount > 0:
            self.credit_amount = self.amount
            self.debit_amount = Decimal(0)
        else:
            self.debit_amount = abs(self.amount)
            self.credit_amount = Decimal(0)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reconciliation: {self.description} - {self.amount}"

    class Meta:
        db_table = "reconciliation"
