from django.shortcuts import render, get_object_or_404

from sales.models import SalesData, Reconciliation


def reconciliation_list(request, sales_data_id):
    # Get the SalesData object
    sales_data = get_object_or_404(SalesData, id=sales_data_id)

    # Filter Reconciliation records related to the given SalesData
    reconciliations = Reconciliation.objects.filter(sales_data=sales_data)

    # Pass the reconciliations and sales_data to the template
    return render(request, 'reconciliation/reconciliation_list.html', {
        'sales_data': sales_data,
        'reconciliations': reconciliations
    })

