from django.shortcuts import render
from django.http import HttpResponse
from .models import Shop, SalesData
import pandas as pd
from django.db.utils import IntegrityError
from django.views.generic import ListView

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
            return redirect('sales_data_list')
             
            # return HttpResponse("File uploaded and data processed successfully.")
        except IntegrityError as e:
            return HttpResponse(f"Error processing file: {e}", status=400)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=400)

    # Pass the list of shops to the template
    return render(request, 'sales/upload.html', {'shops': shops})


# ================Shop CRUD==================
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Shop, SalesData
from .forms import ShopForm

# ✅ List all shops
def shop_list(request):
    shops = Shop.objects.all()
    return render(request, 'shops/shop_list.html', {'shops': shops})

# ✅ Create new shop
def shop_create(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop_list')
    else:
        form = ShopForm()
    return render(request, 'shops/shop_form.html', {'form': form})

# ✅ Update shop
def shop_update(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == 'POST':
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('shop_list')
    else:
        form = ShopForm(instance=shop)
    return render(request, 'shops/shop_form.html', {'form': form})

# ✅ Delete shop
def shop_delete(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == 'POST':
        shop.delete()
        return redirect('shop_list')
    return render(request, 'shops/shop_confirm_delete.html', {'shop': shop})

















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


