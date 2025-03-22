from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..models import Shop, SalesData
import pandas as pd
from django.db.utils import IntegrityError
from django.views.generic import ListView

import pdfplumber

class SalesDataListView(ListView):
    model = SalesData
    template_name = 'sales/sales_data_list.html'
    context_object_name = 'sales_data'

    def get_queryset(self):
        queryset = SalesData.objects.all().order_by('shop', 'date_uploaded')
        
        # # Debugging: Print the sales data to see the structure
        # for sales in queryset:
        #     print(sales.data)  # This will print the data in the terminal/log
        return queryset



# store the entire file data in one JSON field without pdf
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

#             # Group all rows for the selected shop into a single JSON field
#             all_rows = []
#             for index, row in df.iterrows():
#                 # Prepare the row data and filter out empty values
#                 row_data = row.to_dict()
#                 row_data = {key: value for key, value in row_data.items() if pd.notnull(value)}

#                 # Ensure row data is not empty, add to listf
#                 if row_data:
#                     all_rows.append(row_data)

#             # If there are any rows, store the data in the SalesData table for the selected shop
#             if all_rows:
#                 # Use the selected shop and store all rows in the 'data' field as a JSON object
#                 SalesData.objects.create(shop=shop, data=all_rows)
#             return redirect('sales_data_list')
             
#             # return HttpResponse("File uploaded and data processed successfully.")
#         except IntegrityError as e:
#             return HttpResponse(f"Error processing file: {e}", status=400)
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {e}", status=400)

#     # Pass the list of shops to the template
#     return render(request, 'sales/upload.html', {'shops': shops})


# with pdf
import pdfplumber
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..models import SalesData, Shop
from django.db import IntegrityError

def upload_sales_data(request):
    shops = Shop.objects.all()  # Fetch all shops
    all_rows = []  # Initialize all_rows at the start to avoid the "not assigned" error

    if request.method == 'POST' and request.FILES['file']:
        # Get the uploaded file
        file = request.FILES['file']

        try:
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
                # Process Excel data here
                for index, row in df.iterrows():
                    row_data = row.to_dict()
                    # Convert any Timestamp values to strings
                    row_data = {key: value if not isinstance(value, pd.Timestamp) else value.strftime('%Y-%m-%d') 
                                for key, value in row_data.items()}
                    # Remove any null values from row_data
                    row_data = {key: value for key, value in row_data.items() if pd.notnull(value)}
                    if row_data:
                        all_rows.append(row_data)

            elif file.name.endswith('.csv'):
                df = pd.read_csv(file)
                # Process CSV data here
                for index, row in df.iterrows():
                    row_data = row.to_dict()
                    # Convert any Timestamp values to strings
                    row_data = {key: value if not isinstance(value, pd.Timestamp) else value.strftime('%Y-%m-%d') 
                                for key, value in row_data.items()}
                    # Remove any null values from row_data
                    row_data = {key: value for key, value in row_data.items() if pd.notnull(value)}
                    if row_data:
                        all_rows.append(row_data)

            elif file.name.endswith('.pdf'):
                # Handle PDF file
                with pdfplumber.open(file) as pdf:
                    first_page = pdf.pages[0]
                    text = first_page.extract_text()

                    if text:
                        lines = text.split('\n')
                        data_lines = [line for line in lines if line.strip()]
                        for line in data_lines:
                            parts = line.split()
                            if len(parts) > 1:
                                row_data = {}
                                for idx, part in enumerate(parts):
                                    column_name = f"column_{idx+1}"  # Generate dynamic column names
                                    row_data[column_name] = part
                                all_rows.append(row_data)
                    else:
                        return HttpResponse("No valid text found in the PDF.", status=400)

            else:
                return HttpResponse("Invalid file format. Only .csv, .xlsx, and .pdf are supported.", status=400)

            # Get the shop selection from the form
            selected_shop_id = request.POST.get('shop')  # Get the selected shop id
            
            if selected_shop_id:
                shop = Shop.objects.get(id=selected_shop_id)
            else:
                return HttpResponse("Shop is required", status=400)

            # If we have rows, store them in the database as a JSON field
            if all_rows:
                # Use the selected shop and store all rows in the 'data' field as a JSON object
                SalesData.objects.create(shop=shop, data=all_rows)

            return redirect('sales_data_list')

        except IntegrityError as e:
            return HttpResponse(f"Error processing file: {e}", status=400)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=400)

    # Pass the list of shops to the template
    return render(request, 'sales/upload.html', {'shops': shops})
