from sales.models import SalesData, Reconciliation
from django.http import JsonResponse
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

# Reconcile button for SalseData (sales_data_list.html)
@csrf_exempt
def reconcile_sales_data(request, sales_data_id):
    if request.method == "POST":
        # Get the SalesData object by ID or return 404 if not found
        sales_data = get_object_or_404(SalesData, id=sales_data_id)

        # Check if there is data in the SalesData object
        if not sales_data.data:
            return JsonResponse({"success": False, "error": "No data found in SalesData record"})

        # Iterate over each record in the JSON data
        for record in sales_data.data:
            # Normalize the description (trim and lowercase)
            description = record.get("Description", "").strip().lower()

            # Convert the amount to Decimal (default to 0 if missing)
            amount = Decimal(record.get("Amount", "0"))

            try:
                # Try to create a new Reconciliation entry
                # If a duplicate exists (based on unique_together), it will raise IntegrityError
                Reconciliation.objects.create(
                    description=description,
                    amount=amount,
                    sales_data=sales_data  # Link this record to the SalesData instance
                )
            except IntegrityError:
                # Duplicate detected — skip this entry silently
                continue

        # Mark the SalesData record as reconciled
        sales_data.is_reconciled = True
        sales_data.save()

        # Return success response
        return JsonResponse({"success": True, "message": "Reconciliation completed successfully!"})

    # Handle non-POST requests
    return JsonResponse({"success": False, "error": "Invalid request method!"})




# Old code before unique_together = ('sales_data', 'description', 'amount') in Reconciliation model
# @csrf_exempt
# def reconcile_sales_data(request, sales_data_id):
#     if request.method == "POST":
#         sales_data = get_object_or_404(SalesData, id=sales_data_id)

#         if not sales_data.data:
#             return JsonResponse({"success": False, "error": "No data found in SalesData record"})

#         # Extract "Description" and "Amount" from JSON field and insert into Reconciliation table
#         for record in sales_data.data:
#             description = record.get("Description", "").strip().lower()  # Normalize description (trim and lower case)
#             amount = Decimal(record.get("Amount", "0"))  # Extract amount

#             # Check if a reconciliation record with the same normalized description and amount already exists
#             if not Reconciliation.objects.filter(
#                 description__iexact=description, amount=amount, sales_data=sales_data).exists():
#                 # Insert into Reconciliation table and associate with SalesData
#                 Reconciliation.objects.create(
#                     description=description,
#                     amount=amount,
#                     sales_data=sales_data  # Link to the SalesData entry
#                 )
#             # else:
#             #     print(f"Skipping duplicate: {description} with amount {amount}")

#         # Mark SalesData as reconciled
#         sales_data.is_reconciled = True
#         sales_data.save()

#         return JsonResponse({"success": True, "message": "Reconciliation completed successfully!"})

#     return JsonResponse({"success": False, "error": "Invalid request method!"})


