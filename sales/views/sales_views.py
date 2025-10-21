from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..models import Shop, SalesData
import pandas as pd
from django.db.utils import IntegrityError
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


import pdfplumber

class SalesDataListView(LoginRequiredMixin, ListView):
    model = SalesData
    template_name = 'sales/sales_data_list.html'
    context_object_name = 'sales_data'

    def dispatch(self, request, *args, **kwargs):
        # Check if shop is selected
        if 'selected_shop_id' not in request.session:
            return redirect('shop_selection')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Filter by selected shop only
        selected_shop_id = self.request.session.get('selected_shop_id')
        queryset = SalesData.objects.filter(shop_id=selected_shop_id).order_by('-date_uploaded')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get selected shop
        selected_shop_id = self.request.session.get('selected_shop_id')
        selected_shop = Shop.objects.get(id=selected_shop_id)
        
        # Calculate reconciliation statistics
        total_uploads = self.get_queryset().count()
        reconciled_count = 0
        pending_count = 0
        
        for sales_data in self.get_queryset():
            # Check if this sales data is fully reconciled
            reconciliations = sales_data.reconciliation_set.all()
            if reconciliations.exists():
                # Check if all reconciliations have both slicer_new and category_new
                fully_reconciled = all(
                    r.slicer_new and r.slicer_new.strip() and 
                    r.category_new and r.category_new.strip() 
                    for r in reconciliations
                )
                if fully_reconciled:
                    reconciled_count += 1
                else:
                    pending_count += 1
            else:
                pending_count += 1
        
        context.update({
            'selected_shop': selected_shop,
            'total_uploads': total_uploads,
            'reconciled_count': reconciled_count,
            'pending_count': pending_count,
        })
        
        return context



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
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError

def upload_sales_data(request):
    # Check if shop is selected
    if 'selected_shop_id' not in request.session:
        return redirect('shop_selection')
    
    selected_shop_id = request.session.get('selected_shop_id')
    selected_shop = Shop.objects.get(id=selected_shop_id)
    all_rows = []  # Initialize to prevent errors

    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']

        try:
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file, dtype=str)  # Read everything as string
                for index, row in df.iterrows():
                    row_data = row.to_dict()
                    row_data = {
                        key: (value.strftime('%Y-%m-%d') if isinstance(value, pd.Timestamp) else value if pd.notnull(value) else "")
                        for key, value in row_data.items()
                    }
                    all_rows.append(row_data)

            elif file.name.endswith('.csv'):
                df = pd.read_csv(file, dtype=str)  # Read everything as string
                for index, row in df.iterrows():
                    row_data = row.to_dict()
                    all_rows.append(row_data)

            elif file.name.endswith('.pdf'):
                with pdfplumber.open(file) as pdf:
                    extracted_text = ""
                    for page in pdf.pages:
                        extracted_text += page.extract_text() + "\n"

                    if extracted_text.strip():  # Ensure PDF is not empty
                        data_lines = [line.strip() for line in extracted_text.split("\n") if line.strip()]
                        
                        if not data_lines:
                            return HttpResponse("No readable text found in the PDF.", status=400)

                        # Try to extract headers dynamically
                        headers = re.split(r'\s{2,}', data_lines[0]) if len(data_lines) > 0 else []
                        
                        if len(headers) < 2:  # If headers are not found, create default column names
                            headers = [f"column_{i+1}" for i in range(len(data_lines[1].split()))]

                        # Extract rows dynamically
                        for line in data_lines[1:]:
                            row_values = re.split(r'\s{2,}', line)  # Split data by spaces/tabs
                            row_dict = {headers[idx]: value for idx, value in enumerate(row_values) if idx < len(headers)}
                            all_rows.append(row_dict)

                    else:
                        return HttpResponse("PDF is empty or unreadable.", status=400)

            else:
                return HttpResponse("Invalid file format. Only .csv, .xlsx, and .pdf are supported.", status=400)

            if all_rows:  # Ensure we only save if there's data
                SalesData.objects.create(shop=selected_shop, data=all_rows)

            return redirect('sales_data_list')

        except IntegrityError as e:
            return HttpResponse(f"Error processing file: {e}", status=400)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=400)

    return render(request, 'sales/upload.html', {'selected_shop': selected_shop})
