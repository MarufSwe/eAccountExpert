from django import forms
from .models import Shop

class SalesDataForm(forms.Form):
    shop = forms.ModelChoiceField(queryset=Shop.objects.all(), label="Select Shop")
    file = forms.FileField()


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'location', 'owner_name', 'contact_number']
