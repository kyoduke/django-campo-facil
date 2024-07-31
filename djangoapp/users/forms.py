from django import forms
from django.contrib.auth import get_user_model
from .models import User


class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False, label='Nome')
    last_name = forms.CharField(max_length=100, required=False, label='Sobrenome')
    email = forms.EmailField(required=True)


    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        