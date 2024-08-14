from django.shortcuts import render, redirect
from .forms import FootballFieldForm, AddressForm, AttachmentFormSet, FootballFieldFilterForm
from django.http import HttpRequest
from django.contrib import messages
from .models import FootballField, Address
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json

# Create your views here.
@login_required(redirect_field_name='account_login')
def create_football_field(request: HttpRequest):
    if request.method == 'POST':
        field_form = FootballFieldForm(request.POST, request.FILES)
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



@login_required(redirect_field_name='account_login')
def football_field_list(request: HttpRequest):
    form = FootballFieldFilterForm(request.GET or None) 
    fields = FootballField.objects.all()

    addresses = Address.objects.select_related('football_field').all()
    data = []
    for address in addresses:
        if address.latitude and address.longitude:
            data.append({'name': address.football_field.name, 'latitude': float(address.latitude), 'longitude': float(address.longitude)})
    # addresses = Address.objects.all()

    if form.is_valid():
        if form.cleaned_data['city']:
            fields = fields.filter(address__city__icontains=form.cleaned_data['city'])
        if form.cleaned_data['grass_type']:
            fields = fields.filter(grass_type=form.cleaned_data['grass_type'])
        if form.cleaned_data['has_field_lighting']:
            fields = fields.filter(has_field_lighting=form.cleaned_data['has_field_lighting'])
        if form.cleaned_data['has_changing_room']:
            fields = fields.filter(has_changing_room=form.cleaned_data['has_changing_room'])
        if form.cleaned_data['max_hour_price']:
            fields = fields.filter(hour_price__lte=form.cleaned_data['max_hour_price'])

    context = {
        'form': form,
        'fields': fields,
        'addresses': json.dumps(data)
    }
    return render(request, template_name='football_fields/list_football_fields.html', context=context)