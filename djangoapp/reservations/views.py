from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from reservations.forms import ReservationForm
from football_fields.models import FootballField
from django.contrib import messages
from .models import Reservation

# Create your views here.

@login_required(redirect_field_name='account_login')
def create_reservation(request: HttpRequest, pk:int):
    try:
        field = FootballField.objects.get(pk=pk)
    except FootballField.DoesNotExist:
        messages.warning(request, _('Este campo não existe mais.'))
        return redirect('football_field_list')
         
    if request.method == 'POST':
        reservation = Reservation(user=request.user, football_field=field)
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, _('Reservation created successfully.'))
            return redirect(to='football_field_detail', pk=pk)
        else: 
            print(form.errors)
            for error in form.errors:
                print(error)    
                print(form.errors[error])
                
                messages.warning(request, form.errors[error])



    template_name = 'reservations/create.html'
    form = ReservationForm()
    context = {
        'form': form,
        'field': field
    }
    return render(request, template_name=template_name, context=context)


def user_reservations(request: HttpRequest):
    context = {}
    return render(request, 'reservations/user_reservations.html', context=context)