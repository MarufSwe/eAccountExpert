from django.shortcuts import render, redirect, get_object_or_404
from ..models import Shop
from ..forms import ShopForm
from django.contrib.auth.decorators import login_required


# ✅ Shop selection page (landing after login)
@login_required
def shop_selection(request):
    shops = Shop.objects.all()
    return render(request, 'shops/shop_selection.html', {'shops': shops})


# ✅ Handle shop selection
@login_required
def select_shop(request):
    if request.method == 'POST':
        shop_id = request.POST.get('shop_id')
        if shop_id:
            # Store selected shop in session
            request.session['selected_shop_id'] = int(shop_id)
            return redirect('sales_data_list')
    return redirect('shop_selection')


# ✅ List all shops (admin view)
@login_required
def shop_list(request):
    shops = Shop.objects.all()
    return render(request, 'shops/shop_list.html', {'shops': shops})

# ✅ Create new shop
def shop_create(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop_list')
    else:
        form = ShopForm()
    return render(request, 'shops/shop_form.html', {'form': form})

# ✅ Update shop
def shop_update(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == 'POST':
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('shop_list')
    else:
        form = ShopForm(instance=shop)
    return render(request, 'shops/shop_form.html', {'form': form})

# ✅ Delete shop
def shop_delete(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == 'POST':
        shop.delete()
        return redirect('shop_list')
    return render(request, 'shops/shop_confirm_delete.html', {'shop': shop})


