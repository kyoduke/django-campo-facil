from django import forms
from django.contrib.auth import get_user_model
from .models import User
from phonenumber_field.formfields import PhoneNumberField

class UpdateProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False, label='Foto de perfil')
    first_name = forms.CharField(max_length=100, required=False, label='Nome')
    last_name = forms.CharField(max_length=100, required=False, label='Sobrenome')
    email = forms.EmailField(required=True)
    phone_number = PhoneNumberField(region='BR', required=False, label='Celular')


    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_image']
        