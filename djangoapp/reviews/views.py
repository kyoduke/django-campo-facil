from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from reservations.models import Reservation
from football_fields.models import FootballField
from reviews.forms import ReviewForm
from reviews.models import Review



def create_review(request:HttpRequest, pk: int):
    # this view only handles post requests
    if not request.method == 'POST':
        return redirect(to='football_field_detail', pk=pk)

    football_field = None
    try:
        football_field = FootballField.objects.get(pk=pk)

        # create an instance with the two fields we don't want the user to change
        instance = Review(author=request.user, football_field=football_field)
        form = ReviewForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, _('Thank you for posting a review.'))
            return redirect('football_field_detail', pk=pk)

    except FootballField.DoesNotExist:
        messages.warning(request, _('The field you requested doesnt exists anymore.'))
        return redirect(to='football_field_list')

    