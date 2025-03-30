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

    # Query all slicer lists to display in the template
    slicer_lists = SlicerList.objects.all()
    # for slicer in slicer_lists:
    #     print("slicer.name------:", slicer.name)
        
    cat_list_d = CatListD.objects.all()
    cat_list_c = CatListC.objects.all()

    # Filter Reconciliation records related to the given SalesData
    reconciliations = Reconciliation.objects.filter(sales_data=sales_data)

    # Pass the slicer_lists, cat_list_d, and cat_list_c directly to the template
    return render(request, 'reconciliation/reconciliation_list.html', {
        'sales_data': sales_data,
        'reconciliations': reconciliations,
        'slicer_lists': slicer_lists,
        'cat_list_d': cat_list_d,
        'cat_list_c': cat_list_c
    })

