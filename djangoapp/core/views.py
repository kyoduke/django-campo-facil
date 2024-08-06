from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='account_login')
def home_page(request):
    return render(request, 'core/home.html')