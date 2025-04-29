import random
from django.shortcuts import render, get_object_or_404
# from sales.models import CatListC, CatListD, SalesData, Reconciliation, SlicerList
from sales.models import CategoryMapping, SalesData, Reconciliation
import re
import random

def reconciliation_list(request, sales_data_id):
    # Get the specific SalesData object
    sales_data = get_object_or_404(SalesData, id=sales_data_id)

    # Get all CategoryMapping entries
    category_mappings = CategoryMapping.objects.all()

    # Get all Reconciliation records for this SalesData
    reconciliations = Reconciliation.objects.filter(sales_data=sales_data)
    # print("Total reconciliations:", reconciliations.count())

    # Optional: For debugging description uniqueness
    # descriptions = [r.description for r in reconciliations]
    # print("Total descriptions:", len(descriptions))
    # print("Unique descriptions:", len(set(descriptions)))

    # Iterate over each reconciliation record
    for reconciliation in reconciliations:
        matched_mapping = None

        # Find the first matching CategoryMapping based on slicer_list and description
        for mapping in category_mappings:
            pattern = r'\b' + re.escape(mapping.slicer_list.strip()) + r'\b'
            if re.search(pattern, reconciliation.description, re.IGNORECASE):
                matched_mapping = mapping
                break

        # Assign slicer list and category names based on mapping
        reconciliation.slicer_new = matched_mapping.slicer_list if matched_mapping else " "
        reconciliation.slicer_list_name = matched_mapping.slicer_list if matched_mapping else "No slicer list available"
        reconciliation.cat_list_d_name = matched_mapping.cat_list_d if matched_mapping else "No category list D available"
        reconciliation.cat_list_c_name = matched_mapping.cat_list_c if matched_mapping else "No category list C available"

        # Assign category_new based on amount (debit or credit logic)
        if matched_mapping:
            if reconciliation.amount < 0:
                reconciliation.category_new = matched_mapping.cat_list_d
            else:
                reconciliation.category_new = matched_mapping.cat_list_c
        else:
            reconciliation.category_new = " "  # Default if no match

    # Render the reconciliations in the template
    return render(request, 'reconciliation/reconciliation_list.html', {
        'sales_data': sales_data,
        'reconciliations': reconciliations,
        'category_mappings': category_mappings
    })