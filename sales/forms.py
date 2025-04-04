from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Shop, SlicerList, CatListD, CatListC

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


class SlicerListForm(forms.ModelForm):
    class Meta:
        model = SlicerList
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(SlicerListForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = ""  # Set the initial value to an empty string instead of None

class CatListDForm(forms.ModelForm):
    class Meta:
        model = CatListD
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(CatListDForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = ""  # Set the initial value to an empty string

class CatListCForm(forms.ModelForm):
    class Meta:
        model = CatListC
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(CatListCForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = ""  # Set the initial value to an empty string
