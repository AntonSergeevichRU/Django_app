from django import forms
from .models import *





class AddAvatarForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'



    avatar = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )
