from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from football_fields.models import FootballField, Address
from football_fields.forms import (
    FootballFieldForm,
    AddressForm,
    AttachmentFormSet,
    FootballFieldFilterForm,
)
from reservations.models import Reservation
from reviews.forms import ReviewForm
from reviews.models import Review
import json


# only admins can create fields
@login_required(redirect_field_name="account_login")
def create_football_field(request: HttpRequest):
    if not request.user.is_staff:
        return redirect(to="football_field_list")
    if request.method == "POST":
        field_form = FootballFieldForm(request.POST, request.FILES)
        address_form = AddressForm(request.POST)
        attachment_form_set = AttachmentFormSet(data=request.POST, files=request.FILES)
        if (
            field_form.is_valid()
            and address_form.is_valid()
            and attachment_form_set.is_valid()
        ):
            football_field = field_form.save()
            address: Address = address_form.save(commit=False)
            address.football_field = football_field
            address.save()

            attachment_form_set.instance = football_field
            attachment_form_set.save()

            messages.success(request, "Campo de futebol adicionado com sucesso.")
            return redirect(to="football_field_list")
        else:
            return render(
                request,
                "football_fields/create_football_field.html",
                {
                    "field_form": field_form,
                    "address_form": address_form,
                    "attachment_form": attachment_form_set,
                },
            )
    else:
        field_form = FootballFieldForm()
        address_form = AddressForm()
        attachment_form_set = AttachmentFormSet()
        return render(
            request,
            "football_fields/create_football_field.html",
            {
                "field_form": field_form,
                "address_form": address_form,
                "attachment_form": attachment_form_set,
            },
        )


@login_required(redirect_field_name="account_login")
def football_field_list(request: HttpRequest):
    form = FootballFieldFilterForm(request.GET or None)
    fields = FootballField.objects.all()

    if form.is_valid():
        if form.cleaned_data["city"]:
            fields = fields.filter(address__city__icontains=form.cleaned_data["city"])
        if form.cleaned_data["grass_type"]:
            fields = fields.filter(grass_type=form.cleaned_data["grass_type"])
        if form.cleaned_data["has_field_lighting"]:
            fields = fields.filter(
                has_field_lighting=form.cleaned_data["has_field_lighting"]
            )
        if form.cleaned_data["has_changing_room"]:
            fields = fields.filter(
                has_changing_room=form.cleaned_data["has_changing_room"]
            )
        if form.cleaned_data["max_hour_price"]:
            fields = fields.filter(hour_price__lte=form.cleaned_data["max_hour_price"])

    data = []
    for field in fields:
        if field.address.latitude and field.address.longitude:
            data.append(
                {
                    "name": field.name,
                    "latitude": float(field.address.latitude),
                    "longitude": float(field.address.longitude),
                }
            )

    context = {"form": form, "fields": fields, "addresses": json.dumps(data)}
    return render(
        request,
        template_name="football_fields/list_football_fields.html",
        context=context,
    )


@login_required(redirect_field_name="account_login")
def football_field_detail(request: HttpRequest, pk: int):

    try:
        field = FootballField.objects.get(pk=pk)
        reviews = field.reviews.filter(is_active=True)
    except FootballField.DoesNotExist:
        messages.warning(request, "Este campo não existe mais.")
        return redirect(to="football_field_list")

    review_form = None
    # adds a review form if the user have a reservation under this field
    # and the user havent created a review yet.
    if (
        Reservation.objects.filter(
            football_field=pk, user=request.user, status="finished"
        ).exists()
        and not Review.objects.filter(
            football_field=pk, author=request.user, is_active=True
        ).exists()
    ):
        review_form = ReviewForm(initial={"football_field": pk})

    # mean of reviews
    ratings = [review.rating for review in reviews]
    ratings_mean = round(sum(ratings) / len(reviews), 1) if not len(ratings) == 0 else 5
    context = {
        "field": field,
        "review_form": review_form,
        "reviews": reviews,
        "ratings_mean": ratings_mean,
    }

    return render(request, "football_fields/detail.html", context)
