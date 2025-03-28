# import json
# from decimal import Decimal
# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from django.views.decorators.csrf import csrf_exempt

# from sales.models import SalesData, Reconciliation


# @csrf_exempt
# def reconcile_sales_data(request, sales_data_id):
#     if request.method == "POST":
#         sales_data = get_object_or_404(SalesData, id=sales_data_id)

#         if not sales_data.data:
#             return JsonResponse({"success": False, "error": "No data found in SalesData record"})

#         # Extract "Description" and "Amount" from JSON field
#         for record in sales_data.data:
#             description = record.get("Description", "")  # Extract description
#             amount = Decimal(record.get("Amount", "0"))  # Extract amount

#             # Insert into Reconciliation table
#             Reconciliation.objects.create(
#                 description=description,
#                 amount=amount
#             )

#         return JsonResponse({"success": True, "message": "Reconciliation completed successfully!"})

#     return JsonResponse({"success": False, "error": "Invalid request method!"})



import json
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from sales.models import SalesData, Reconciliation



@csrf_exempt
def reconcile_sales_data(request, sales_data_id):
    if request.method == "POST":
        sales_data = get_object_or_404(SalesData, id=sales_data_id)

        if not sales_data.data:
            return JsonResponse({"success": False, "error": "No data found in SalesData record"})

        # Extract "Description" and "Amount" from JSON field
        for record in sales_data.data:
            description = record.get("Description", "")  # Extract description
            amount = Decimal(record.get("Amount", "0"))  # Extract amount

            # Insert into Reconciliation table and associate with SalesData
            Reconciliation.objects.create(
                description=description,
                amount=amount,
                sales_data=sales_data  # Link to the SalesData entry
            )

        return JsonResponse({"success": True, "message": "Reconciliation completed successfully!"})

    return JsonResponse({"success": False, "error": "Invalid request method!"})
