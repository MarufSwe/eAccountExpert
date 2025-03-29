from sales.models import SalesData, Reconciliation
from django.http import JsonResponse
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
# from .models import SalesData, Reconciliation

@csrf_exempt
def reconcile_sales_data(request, sales_data_id):
    if request.method == "POST":
        sales_data = get_object_or_404(SalesData, id=sales_data_id)

        if not sales_data.data:
            return JsonResponse({"success": False, "error": "No data found in SalesData record"})

        # Extract "Description" and "Amount" from JSON field and insert into Reconciliation table
        for record in sales_data.data:
            description = record.get("Description", "")  # Extract description
            amount = Decimal(record.get("Amount", "0"))  # Extract amount

            # Insert into Reconciliation table and associate with SalesData
            Reconciliation.objects.create(
                description=description,
                amount=amount,
                sales_data=sales_data  # Link to the SalesData entry
            )

        # Mark SalesData as reconciled
        sales_data.is_reconciled = True
        sales_data.save()

        return JsonResponse({"success": True, "message": "Reconciliation completed successfully!"})

    return JsonResponse({"success": False, "error": "Invalid request method!"})
