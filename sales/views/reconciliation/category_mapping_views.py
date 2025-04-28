from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from sales.forms import CategoryMappingForm
from sales.models import CategoryMapping


# List all entries
# def category_mapping_list(request):
#     mappings = CategoryMapping.objects.all()
#     return render(request, 'reconciliation/category_mapping/category_mapping_list.html', {'mappings': mappings})

def category_mapping_list(request):
    search_query = request.GET.get('search', '')  # Get the search query from GET request by 3 fields
    if search_query:
        mappings = CategoryMapping.objects.filter(
            Q(slicer_list__icontains=search_query) |
            Q(cat_list_d__icontains=search_query) |
            Q(cat_list_c__icontains=search_query)
        )
    else:
        mappings = CategoryMapping.objects.all()  # If no search, return all

    return render(request, 'reconciliation/category_mapping/category_mapping_list.html', {
        'mappings': mappings,
        'search_query': search_query,  # Pass the search query back to the template
    })


# Create new entry
def category_mapping_create(request):
    if request.method == 'POST':
        form = CategoryMappingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_mapping_list')
    else:
        form = CategoryMappingForm()
    return render(request, 'reconciliation/category_mapping/category_mapping_form.html', {'form': form})

# Update existing entry
def category_mapping_update(request, pk):
    mapping = get_object_or_404(CategoryMapping, pk=pk)
    if request.method == 'POST':
        form = CategoryMappingForm(request.POST, instance=mapping)
        if form.is_valid():
            form.save()
            return redirect('category_mapping_list')
    else:
        form = CategoryMappingForm(instance=mapping)
    return render(request, 'reconciliation/category_mapping/category_mapping_form.html', {'form': form})

# Delete entry
def category_mapping_delete(request, pk):
    mapping = get_object_or_404(CategoryMapping, pk=pk)
    if request.method == 'POST':
        mapping.delete()
        return redirect('category_mapping_list')
    return render(request, 'category_mapping_confirm_delete.html', {'mapping': mapping})
