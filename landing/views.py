from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def landing_page(request):
    """
    Landing page for non-authenticated users showing company services
    """
    return render(request, 'landing/index.html')

@login_required
def dashboard_redirect(request):
    """
    Redirect to dashboard - requires login
    """
    from django.shortcuts import redirect
    return redirect('sales_data_list')