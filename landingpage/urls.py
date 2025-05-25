from django.urls import path
from landingpage.views.landingpage_views import *
urlpatterns = [
 path('', landing_page, name='landing-page'),
]