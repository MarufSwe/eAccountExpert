import random
from django.shortcuts import render, get_object_or_404

from sales.models import CatListC, CatListD, SalesData, Reconciliation, SlicerList


# def reconciliation_list(request, sales_data_id):
#     # Get the SalesData object
#     sales_data = get_object_or_404(SalesData, id=sales_data_id)

#     # Query all slicer lists to display in the template
#     slicer_lists = SlicerList.objects.all()
#     # Iterating over the queryset to print each name
#     for slicer in slicer_lists:
#         print("slicer.name------:", slicer.name)

#     cat_list_d = CatListD.objects.all()
#     cat_list_c = CatListC.objects.all()


#     new_datas = {
#     'slicer_lists': slicer_lists,
#     'cat_list_d': cat_list_d,
#     'cat_list_c': cat_list_c,
#     }

#     # Filter Reconciliation records related to the given SalesData
#     reconciliations = Reconciliation.objects.filter(sales_data=sales_data)

#     # Pass the reconciliations and sales_data to the template
#     return render(request, 'reconciliation/reconciliation_list.html', {
#         'sales_data': sales_data,
#         'reconciliations': reconciliations,
#         'new_datas': new_datas
#     })


def reconciliation_list(request, sales_data_id):
    # Get the SalesData object
    sales_data = get_object_or_404(SalesData, id=sales_data_id)

    # Filter Reconciliation records related to the given SalesData
    reconciliations = Reconciliation.objects.filter(sales_data=sales_data)

    # Query all slicer lists to display in the template
    slicer_lists = SlicerList.objects.all()
    cat_list_d = CatListD.objects.all()
    cat_list_c = CatListC.objects.all()


    # Randomly assign slicer_list, cat_list_d, and cat_list_c for each reconciliation
    for reconciliation in reconciliations:
        reconciliation.slicer_list_name = random.choice(slicer_lists).name if slicer_lists else 'No slicer list available'
        reconciliation.cat_list_d_name = random.choice(cat_list_d).name if cat_list_d else 'No CatListD available'
        reconciliation.cat_list_c_name = random.choice(cat_list_c).name if cat_list_c else 'No CatListC available'

    # Pass the slicer_lists, cat_list_d, and cat_list_c directly to the template
    return render(request, 'reconciliation/reconciliation_list.html', {
        'sales_data': sales_data,
        'reconciliations': reconciliations,
        'slicer_lists': slicer_lists,
        'cat_list_d': cat_list_d,
        'cat_list_c': cat_list_c
    })

