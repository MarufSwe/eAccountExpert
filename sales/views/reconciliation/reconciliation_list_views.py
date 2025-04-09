import random
from django.shortcuts import render, get_object_or_404
from sales.models import CatListC, CatListD, SalesData, Reconciliation, SlicerList
import re
import random

def reconciliation_list(request, sales_data_id):
    sales_data = get_object_or_404(SalesData, id=sales_data_id)
    
    slicer_lists = SlicerList.objects.all()
    cat_list_d = CatListD.objects.all()
    cat_list_c = CatListC.objects.all()

    reconciliations = Reconciliation.objects.filter(sales_data=sales_data)

    for reconciliation in reconciliations:
        matched_slicer = None
        for slicer in slicer_lists:
            # Escape special characters in slicer.name and add word boundaries
            pattern = r'\b' + re.escape(slicer.name.strip()) + r'\b'
            if re.search(pattern, reconciliation.description, re.IGNORECASE):
                matched_slicer = slicer.name
                break

        reconciliation.slicer_new = matched_slicer if matched_slicer else " "
        reconciliation.slicer_list_name = random.choice(slicer_lists).name if slicer_lists else 'No slicer list available'
        reconciliation.cat_list_d_name = random.choice(cat_list_d).name if cat_list_d else 'No category list D available'
        reconciliation.cat_list_c_name = random.choice(cat_list_c).name if cat_list_c else 'No category list C available'

    return render(request, 'reconciliation/reconciliation_list.html', {
        'sales_data': sales_data,
        'reconciliations': reconciliations,
        'slicer_lists': slicer_lists,
        'cat_list_d': cat_list_d,
        'cat_list_c': cat_list_c
    })


# with category_new logic
# def reconciliation_list(request, sales_data_id):
#     sales_data = get_object_or_404(SalesData, id=sales_data_id)
    
#     slicer_lists = SlicerList.objects.all()
#     cat_list_d = CatListD.objects.all()
#     cat_list_c = CatListC.objects.all()

#     reconciliations = Reconciliation.objects.filter(sales_data=sales_data)

#     for reconciliation in reconciliations:
#         matched_slicer = None
#         matched_category = None
        
#         # 1️⃣ Matching logic for slicer_new (slicer list match)
#         for slicer in slicer_lists:
#             pattern = r'\b' + re.escape(slicer.name.strip()) + r'\b'
#             if re.search(pattern, reconciliation.description, re.IGNORECASE):
#                 matched_slicer = slicer.name
#                 break

#         # 2️⃣ If slicer_new matched, find the corresponding category_new from cat_list_d
#         if matched_slicer:
#             for cat in cat_list_d:
#                 # Here, assuming you want to match the category by some criteria (like name)
#                 if re.search(r'\b' + re.escape(cat.name.strip()) + r'\b', matched_slicer, re.IGNORECASE):
#                     matched_category = cat.name
#                     break

#         reconciliation.slicer_new = matched_slicer if matched_slicer else "------------"
#         reconciliation.category_new = matched_category if matched_category else "----------"

#         # 3️⃣ Random slicer list name and category values for display in extra columns
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
#     # Get the SalesData object
#     sales_data = get_object_or_404(SalesData, id=sales_data_id)

#     # Query all slicer lists, cat_list_d, and cat_list_c to display in the template
#     slicer_lists = SlicerList.objects.all()
#     cat_list_d = CatListD.objects.all()
#     cat_list_c = CatListC.objects.all()

#     # Filter Reconciliation records related to the given SalesData
#     reconciliations = Reconciliation.objects.filter(sales_data=sales_data)

#     # Pass the reconciliations and all lists to the template
#     return render(request, 'reconciliation/reconciliation_list.html', {
#         'sales_data': sales_data,
#         'reconciliations': reconciliations,  # 185 rows based on descriptions
#         'slicer_lists': slicer_lists,        # Full slicer list (470 or so items)
#         'cat_list_d': cat_list_d,            # Full cat list D (470 or so items)
#         'cat_list_c': cat_list_c            # Full cat list C (470 or so items)
#     })
