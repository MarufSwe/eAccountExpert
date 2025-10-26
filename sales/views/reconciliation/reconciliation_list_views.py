import random
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from functools import wraps
# from sales.models import CatListC, CatListD, SalesData, Reconciliation, SlicerList
from sales.models import CategoryMapping, SalesData, Reconciliation
import re
import random
import json


def ajax_login_required(view_func):
    """
    Decorator for AJAX views that require authentication.
    Returns JSON error instead of redirecting to login page.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

# def reconciliation_list(request, sales_data_id):
#     # Get the specific SalesData object
#     sales_data = get_object_or_404(SalesData, id=sales_data_id)

#     # Get all CategoryMapping entries
#     category_mappings = CategoryMapping.objects.all()

#     # Get all Reconciliation records for this SalesData
#     reconciliations = Reconciliation.objects.filter(sales_data=sales_data)
#     # print("Total reconciliations:", reconciliations.count())

#     # Optional: For debugging description uniqueness
#     # descriptions = [r.description for r in reconciliations]
#     # print("Total descriptions:", len(descriptions))
#     # print("Unique descriptions:", len(set(descriptions)))

#     # Iterate over each reconciliation record
#     for reconciliation in reconciliations:
#         matched_mapping = None

#         # Find the first matching CategoryMapping based on slicer_list and description
#         for mapping in category_mappings:
#             pattern = r'\b' + re.escape(mapping.slicer_list.strip()) + r'\b'
#             if re.search(pattern, reconciliation.description, re.IGNORECASE):
#                 matched_mapping = mapping
#                 break

#         # Assign slicer list and category names based on mapping
#         reconciliation.slicer_new = matched_mapping.slicer_list if matched_mapping else " "
#         reconciliation.slicer_list_name = matched_mapping.slicer_list if matched_mapping else "No slicer list available"
#         reconciliation.cat_list_d_name = matched_mapping.cat_list_d if matched_mapping else "No category list D available"
#         reconciliation.cat_list_c_name = matched_mapping.cat_list_c if matched_mapping else "No category list C available"

#         # Assign category_new based on amount (debit or credit logic)
#         if matched_mapping:
#             if reconciliation.amount < 0:
#                 reconciliation.category_new = matched_mapping.cat_list_d
#             else:
#                 reconciliation.category_new = matched_mapping.cat_list_c
#         else:
#             reconciliation.category_new = " "  # Default if no match

#     # Render the reconciliations in the template
#     return render(request, 'reconciliation/reconciliation_list.html', {
#         'sales_data': sales_data,
#         'reconciliations': reconciliations,
#         'category_mappings': category_mappings
#     })




def reconciliation_list(request, sales_data_id):
    # Get the SalesData instance
    sales_data = get_object_or_404(SalesData, id=sales_data_id)

    # Get all category mappings
    category_mappings = CategoryMapping.objects.all()

    # Get all reconciliations for the current SalesData
    reconciliations = Reconciliation.objects.filter(sales_data=sales_data)
    
    # Get unique category options for dropdown (Cat_List_d for debits, Cat_List_c for credits)
    cat_list_d_options = list(set(mapping.cat_list_d for mapping in category_mappings if mapping.cat_list_d))
    cat_list_c_options = list(set(mapping.cat_list_c for mapping in category_mappings if mapping.cat_list_c))
    
    # Combine and sort all unique categories
    all_category_options = sorted(list(set(cat_list_d_options + cat_list_c_options)))

    # Assign slicer/category info to each reconciliation entry
    for reconciliation in reconciliations:
        matched_mapping = None

        # Only auto-assign if fields are empty
        if not reconciliation.slicer_new or not reconciliation.category_new:
            # Match description with slicer_list using EXACT EXCEL LOGIC (substring search)
            # Sort by length (longest first) to prioritize more specific matches
            sorted_mappings = sorted(category_mappings, key=lambda x: len(x.slicer_list.strip()), reverse=True)
            
            for mapping in sorted_mappings:
                slicer_keyword = mapping.slicer_list.strip().upper()
                description_upper = reconciliation.description.upper()
                
                # Excel formula: COUNTIF(C3,"*"&$M$2:$M$499&"*") - substring search
                if slicer_keyword in description_upper:
                    matched_mapping = mapping
                    break

            # Assign matched slicer/category names (if found) and save to database
            if matched_mapping:
                if not reconciliation.slicer_new:
                    reconciliation.slicer_new = matched_mapping.slicer_list
                    
                if not reconciliation.category_new:
                    # Assign category_new based on debit/credit
                    if reconciliation.amount < 0:
                        reconciliation.category_new = matched_mapping.cat_list_d
                    else:
                        reconciliation.category_new = matched_mapping.cat_list_c
                
                # Save the changes to database
                reconciliation.save()

        # Set display attributes for template (these are not saved to DB)
        reconciliation.slicer_list_name = reconciliation.slicer_new if reconciliation.slicer_new else "No slicer list available"
        reconciliation.cat_list_d_name = reconciliation.category_new if reconciliation.category_new else "No category list D available"
        reconciliation.cat_list_c_name = reconciliation.category_new if reconciliation.category_new else "No category list C available"

    # Generate pivot summary for reconciled and unreconciled transactions
    pivot_summary = {
        'reconciled': {'dr': 0, 'cr': 0},
        'unreconciled': {'dr': 0, 'cr': 0},
    }

    for reconciliation in reconciliations:
        # Determine if this entry is reconciled (has both slicer and category)
        is_reconciled = reconciliation.slicer_new and reconciliation.slicer_new.strip() and reconciliation.category_new and reconciliation.category_new.strip()

        if reconciliation.amount < 0:
            # Debit
            if is_reconciled:
                pivot_summary['reconciled']['dr'] += abs(reconciliation.amount)
            else:
                pivot_summary['unreconciled']['dr'] += abs(reconciliation.amount)
        else:
            # Credit
            if is_reconciled:
                pivot_summary['reconciled']['cr'] += reconciliation.amount
            else:
                pivot_summary['unreconciled']['cr'] += reconciliation.amount
    # Render the result in template
    return render(request, 'reconciliation/reconciliation_list.html', {
        'sales_data': sales_data,
        'reconciliations': reconciliations,
        'category_mappings': category_mappings,
        'pivot_summary': pivot_summary,
        'all_category_options': all_category_options,
        'cat_list_d_options': cat_list_d_options,
        'cat_list_c_options': cat_list_c_options,
    })


@ajax_login_required
@csrf_exempt
def update_reconciliation_field(request, reconciliation_id):
    """Update slicer_new or category_new field for a reconciliation record"""
    
    # Only accept POST requests
    if request.method != 'POST':
        return JsonResponse({"success": False, "error": "Only POST requests allowed"}, status=405)
    
    try:
        reconciliation = get_object_or_404(Reconciliation, id=reconciliation_id)
        
        # Get the field name and value from the request
        field_name = request.POST.get('field_name')
        field_value = request.POST.get('field_value', '').strip()
        
        # Debug logging
        print(f"Updating reconciliation {reconciliation_id}: {field_name} = '{field_value}'")
        print(f"User: {request.user}")
        print(f"POST data: {request.POST}")
        
        # Validate field name
        if field_name not in ['slicer_new', 'category_new']:
            return JsonResponse({"success": False, "error": "Invalid field name"}, status=400)
        
        # Update the field
        setattr(reconciliation, field_name, field_value)
        reconciliation.save()
        
        # Verify the save worked
        reconciliation.refresh_from_db()
        saved_value = getattr(reconciliation, field_name)
        print(f"Saved value: '{saved_value}'")
        
        return JsonResponse({
            "success": True, 
            "message": f"{field_name} updated successfully",
            "new_value": saved_value
        })
        
    except Reconciliation.DoesNotExist:
        print(f"Reconciliation {reconciliation_id} not found")
        return JsonResponse({"success": False, "error": "Reconciliation not found"}, status=404)
    except Exception as e:
        print(f"Error updating reconciliation field: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({"success": False, "error": str(e)}, status=500)
