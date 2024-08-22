from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import UserChangeForm
from .forms import UpdateProfileForm
from django.contrib import messages

import logging
from django.conf import settings
# Create your views here.
fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

logging.basicConfig(format=fmt, level=lvl)

# @login_required(redirect_field_name='account_login')
# def home_view(request: HttpRequest):
#     return render(request, 'base.html')


@login_required(redirect_field_name='account_login')
def user_profile_view(request: HttpRequest):
    if request.method == 'POST':
        user_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso.')
            return redirect(to='profile')
        else:
            new_form = UpdateProfileForm(instance=request.user)
            messages.warning(request, 'Formulário inválido.')
            return redirect(to='profile')
    
    form = UpdateProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})
    
