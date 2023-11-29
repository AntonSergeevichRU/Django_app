from _ast import pattern

from django import forms
from django.core import validators
from.models import *



class AddProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'discount', 'preview']


    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'



class CSVImportForm(forms.Form):
    csv_file = forms.FileField()

