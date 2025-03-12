from django.shortcuts import render
from django.http import HttpResponse
from .models import Shop, SalesData
import pandas as pd
from django.db.utils import IntegrityError


# # storing each transaction as a separate row with duplicate shop names
# def upload_sales_data(request):
#     shops = Shop.objects.all()  # Fetch all shops

#     if request.method == 'POST' and request.FILES['file']:
#         print(request.POST)  # Debugging: Print the form data to see if 'shop' is included

#         # Get the uploaded file
#         file = request.FILES['file']
#         try:
#             if file.name.endswith('.xlsx'):
#                 df = pd.read_excel(file)
#             elif file.name.endswith('.csv'):
#                 df = pd.read_csv(file)
#             else:
#                 return HttpResponse("Invalid file format.", status=400)

#             # Get the shop selection from the form
#             selected_shop_id = request.POST.get('shop')  # Get the selected shop id
            
#             if selected_shop_id:
#                 shop = Shop.objects.get(id=selected_shop_id)
#             else:
#                 return HttpResponse("Shop is required", status=400)

#             # Loop through each row and create SalesData entry
#             for index, row in df.iterrows():
#                 # Prepare the row data and filter out empty values
#                 row_data = row.to_dict()
#                 row_data = {key: value for key, value in row_data.items() if pd.notnull(value)}

#                 # Ensure row data is not empty, create SalesData
#                 if row_data:
#                     SalesData.objects.create(shop=shop, data=row_data)
             
#             return HttpResponse("File uploaded and data processed successfully.")
#         except IntegrityError as e:
#             return HttpResponse(f"Error processing file: {e}", status=400)
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {e}", status=400)

#     # Pass the list of shops to the template
#     return render(request, 'sales/upload.html', {'shops': shops})



# store the entire file data in one JSON field with single shop name
def upload_sales_data(request):
    shops = Shop.objects.all()  # Fetch all shops

    if request.method == 'POST' and request.FILES['file']:
        print(request.POST)  # Debugging: Print the form data to see if 'shop' is included

        # Get the uploaded file
        file = request.FILES['file']
        try:
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            elif file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                return HttpResponse("Invalid file format.", status=400)

            # Get the shop selection from the form
            selected_shop_id = request.POST.get('shop')  # Get the selected shop id
            
            if selected_shop_id:
                shop = Shop.objects.get(id=selected_shop_id)
            else:
                return HttpResponse("Shop is required", status=400)

            # Group all rows for the selected shop into a single JSON field
            all_rows = []
            for index, row in df.iterrows():
                # Prepare the row data and filter out empty values
                row_data = row.to_dict()
                row_data = {key: value for key, value in row_data.items() if pd.notnull(value)}

                # Ensure row data is not empty, add to listf
                if row_data:
                    all_rows.append(row_data)

            # If there are any rows, store the data in the SalesData table for the selected shop
            if all_rows:
                # Use the selected shop and store all rows in the 'data' field as a JSON object
                SalesData.objects.create(shop=shop, data=all_rows)
             
            return HttpResponse("File uploaded and data processed successfully.")
        except IntegrityError as e:
            return HttpResponse(f"Error processing file: {e}", status=400)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=400)

    # Pass the list of shops to the template
    return render(request, 'sales/upload.html', {'shops': shops})
