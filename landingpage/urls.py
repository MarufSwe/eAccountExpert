from django.urls import path
from landingpage.views.landingpage_views import *
from landingpage.views.contact_views import *
urlpatterns = [
 path('', landing_page, name='landing-page'),
 path('contact', contact_views, name='contact-page'),
]