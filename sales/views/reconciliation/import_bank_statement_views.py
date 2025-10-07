# # views.py

# import pandas as pd
# from django.shortcuts import render, redirect
# from django.core.files.storage import FileSystemStorage

# from sales.models import ReconciliationData


# def import_bank_statement(request):
#     if request.method == "POST" and request.FILES["file"]:
#         uploaded_file = request.FILES["file"]
        
#         # Save file temporarily
#         fs = FileSystemStorage()
#         filename = fs.save(uploaded_file.name, uploaded_file)
#         file_path = fs.path(filename)

#         # Read XLSX file
#         df = pd.read_excel(file_path, engine="openpyxl")

#         # Check if required columns exist
#         if "Description" not in df.columns or "Amount" not in df.columns:
#             return render(request, "import_bank_statement.html", {"error": "Missing required columns"})

#         # Loop through rows and create ReconciliationData records
#         for _, row in df.iterrows():
#             description = row["Description"]
#             amount = row["Amount"]

#             # Create ReconciliationData entry
#             ReconciliationData.objects.create(
#                 description=description,
#                 amount=amount,
#             )

#         return redirect("sales_data_list")  # Redirect after import

#     return render(request, "reconciliation/import_bank_statement.html")
