from django.shortcuts import render, redirect
from .forms import FootballFieldForm, AddressForm, AttachmentFormSet
from django.http import HttpRequest
from django.contrib import messages
from .models import FootballField, Address

# Create your views here.
def create_football_field(request: HttpRequest):
    if request.method == 'POST':
        field_form = FootballFieldForm(request.POST)
        address_form = AddressForm(request.POST)
        attachment_form_set = AttachmentFormSet(data=request.POST, files=request.FILES)
        if field_form.is_valid() and address_form.is_valid() and attachment_form_set.is_valid():
            football_field = field_form.save()
            address:Address = address_form.save(commit=False)
            address.football_field = football_field
            address.save()

            attachment_form_set.instance = football_field
            attachment_form_set.save()

            messages.success(request, 'Campo de futebol adicionado com sucesso.')
            return redirect(to='home')
        else:
            return render(request, 'football_fields/create_football_field.html', {
            'field_form': field_form,
            'address_form': address_form,
            'attachment_form': attachment_form_set
            }) 
    else:
        field_form = FootballFieldForm()
        address_form = AddressForm()
        attachment_form_set = AttachmentFormSet()
        return render(request, 'football_fields/create_football_field.html', {
            'field_form': field_form,
            'address_form': address_form,
            'attachment_form': attachment_form_set
        })