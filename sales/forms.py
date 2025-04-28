from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Shop, CategoryMapping

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class SalesDataForm(forms.Form):
    shop = forms.ModelChoiceField(queryset=Shop.objects.all(), label="Select Shop")
    file = forms.FileField()

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'location', 'owner_name', 'contact_number']


class CategoryMappingForm(forms.ModelForm):
    class Meta:
        model = CategoryMapping
        fields = ['slicer_list', 'cat_list_d', 'cat_list_c']
        labels = {
            'slicer_list': 'Slicer name',
            'cat_list_d': 'Cat list D',
            'cat_list_c': 'Cat list C',
        }