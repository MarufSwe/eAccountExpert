from django.shortcuts import render

def contact_views(request):
    return render(request,'landingpage/contact.html')