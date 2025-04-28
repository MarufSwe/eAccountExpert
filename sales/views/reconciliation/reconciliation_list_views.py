import random
from django.shortcuts import render, get_object_or_404
# from sales.models import CatListC, CatListD, SalesData, Reconciliation, SlicerList
from sales.models import CategoryMapping, SalesData, Reconciliation
import re
import random

# def reconciliation_list(request, sales_data_id):
#     sales_data = get_object_or_404(SalesData, id=sales_data_id)
    
#     slicer_lists = SlicerList.objects.all()
#     cat_list_d = CatListD.objects.all()
#     cat_list_c = CatListC.objects.all()

#     reconciliations = Reconciliation.objects.filter(sales_data=sales_data)

#     for reconciliation in reconciliations:
#         matched_slicer = None
#         for slicer in slicer_lists:
#             # Escape special characters in slicer.name and add word boundaries
#             pattern = r'\b' + re.escape(slicer.name.strip()) + r'\b'
#             if re.search(pattern, reconciliation.description, re.IGNORECASE):
#                 matched_slicer = slicer.name
#                 break

#         reconciliation.slicer_new = matched_slicer if matched_slicer else " "
#         reconciliation.slicer_list_name = random.choice(slicer_lists).name if slicer_lists else 'No slicer list available'
#         reconciliation.cat_list_d_name = random.choice(cat_list_d).name if cat_list_d else 'No category list D available'
#         reconciliation.cat_list_c_name = random.choice(cat_list_c).name if cat_list_c else 'No category list C available'

#     return render(request, 'reconciliation/reconciliation_list.html', {
#         'sales_data': sales_data,
#         'reconciliations': reconciliations,
#         'slicer_lists': slicer_lists,
#         'cat_list_d': cat_list_d,
#         'cat_list_c': cat_list_c
#     })


# def reconciliation_list(request, sales_data_id):
#     sales_data = get_object_or_404(SalesData, id=sales_data_id)
    
#     category_mappings = CategoryMapping.objects.all()
#     reconciliations = Reconciliation.objects.filter(sales_data=sales_data)

#     for reconciliation in reconciliations:
#         matched_mapping = None
#         for mapping in category_mappings:
#             # Escape special characters in mapping.slicer_list and add word boundaries
#             pattern = r'\b' + re.escape(mapping.slicer_list.strip()) + r'\b'
#             if re.search(pattern, reconciliation.description, re.IGNORECASE):
#                 matched_mapping = mapping
#                 break

#         reconciliation.slicer_new = matched_mapping.slicer_list if matched_mapping else " "
#         reconciliation.slicer_list_name = matched_mapping.slicer_list if matched_mapping else "No slicer list available"
#         reconciliation.cat_list_d_name = matched_mapping.cat_list_d if matched_mapping else "No category list D available"
#         reconciliation.cat_list_c_name = matched_mapping.cat_list_c if matched_mapping else "No category list C available"

#     return render(request, 'reconciliation/reconciliation_list.html', {
#         'sales_data': sales_data,
#         'reconciliations': reconciliations,
#         'category_mappings': category_mappings
#     })



def reconciliation_list(request, sales_data_id):
    sales_data = get_object_or_404(SalesData, id=sales_data_id)
    
    category_mappings = CategoryMapping.objects.all()
    reconciliations = Reconciliation.objects.filter(sales_data=sales_data)

    for reconciliation in reconciliations:
        matched_mapping = None
        for mapping in category_mappings:
            # Escape special characters in mapping.slicer_list and add word boundaries
            pattern = r'\b' + re.escape(mapping.slicer_list.strip()) + r'\b'
            if re.search(pattern, reconciliation.description, re.IGNORECASE):
                matched_mapping = mapping
                break

        reconciliation.slicer_new = matched_mapping.slicer_list if matched_mapping else " "
        reconciliation.slicer_list_name = matched_mapping.slicer_list if matched_mapping else "No slicer list available"
        reconciliation.cat_list_d_name = matched_mapping.cat_list_d if matched_mapping else "No category list D available"
        reconciliation.cat_list_c_name = matched_mapping.cat_list_c if matched_mapping else "No category list C available"
        
        # Add category_new logic
        if matched_mapping:
            if reconciliation.amount >= 0:
                reconciliation.category_new = matched_mapping.cat_list_d
            else:
                reconciliation.category_new = matched_mapping.cat_list_c
        else:
            reconciliation.category_new = ""

    return render(request, 'reconciliation/reconciliation_list.html', {
        'sales_data': sales_data,
        'reconciliations': reconciliations,
        'category_mappings': category_mappings,
    })
