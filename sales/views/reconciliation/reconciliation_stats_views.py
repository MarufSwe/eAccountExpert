from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from sales.models import SalesData, Reconciliation, CategoryMapping


def reconciliation_stats(request, sales_data_id):
    """
    Display reconciliation statistics and matching effectiveness
    """
    sales_data = get_object_or_404(SalesData, id=sales_data_id)
    reconciliations = Reconciliation.objects.filter(sales_data=sales_data)
    
    # Calculate statistics
    total_records = reconciliations.count()
    auto_matched = reconciliations.filter(
        slicer_new__isnull=False, 
        category_new__isnull=False
    ).exclude(
        slicer_new__exact='', 
        category_new__exact=''
    ).count()
    
    manual_needed = total_records - auto_matched
    match_rate = (auto_matched / total_records * 100) if total_records > 0 else 0
    
    # Amount statistics
    total_amount = sum(abs(r.amount) for r in reconciliations)
    auto_matched_amount = sum(
        abs(r.amount) for r in reconciliations 
        if r.slicer_new and r.slicer_new.strip() and r.category_new and r.category_new.strip()
    )
    
    amount_match_rate = (auto_matched_amount / total_amount * 100) if total_amount > 0 else 0
    
    # Category breakdown
    category_stats = {}
    for recon in reconciliations:
        if recon.category_new and recon.category_new.strip():
            category = recon.category_new
            if category not in category_stats:
                category_stats[category] = {'count': 0, 'amount': 0}
            category_stats[category]['count'] += 1
            category_stats[category]['amount'] += abs(recon.amount)
    
    # Top unmatched descriptions (for improving mapping)
    unmatched_descriptions = [
        r.description[:100] + ('...' if len(r.description) > 100 else '')
        for r in reconciliations 
        if not (r.slicer_new and r.slicer_new.strip() and r.category_new and r.category_new.strip())
    ][:10]
    
    context = {
        'sales_data': sales_data,
        'stats': {
            'total_records': total_records,
            'auto_matched': auto_matched,
            'manual_needed': manual_needed,
            'match_rate': round(match_rate, 2),
            'total_amount': total_amount,
            'auto_matched_amount': auto_matched_amount,
            'amount_match_rate': round(amount_match_rate, 2),
        },
        'category_stats': dict(sorted(category_stats.items(), key=lambda x: x[1]['amount'], reverse=True)),
        'unmatched_descriptions': unmatched_descriptions,
        'total_mapping_rules': CategoryMapping.objects.count(),
    }
    
    return render(request, 'reconciliation/reconciliation_stats.html', context)


def reconciliation_stats_json(request, sales_data_id):
    """
    Return reconciliation statistics as JSON for AJAX calls
    """
    sales_data = get_object_or_404(SalesData, id=sales_data_id)
    reconciliations = Reconciliation.objects.filter(sales_data=sales_data)
    
    total_records = reconciliations.count()
    auto_matched = reconciliations.filter(
        slicer_new__isnull=False, 
        category_new__isnull=False
    ).exclude(
        slicer_new__exact='', 
        category_new__exact=''
    ).count()
    
    manual_needed = total_records - auto_matched
    match_rate = (auto_matched / total_records * 100) if total_records > 0 else 0
    
    return JsonResponse({
        'total_records': total_records,
        'auto_matched': auto_matched,
        'manual_needed': manual_needed,
        'match_rate': round(match_rate, 2),
    })
