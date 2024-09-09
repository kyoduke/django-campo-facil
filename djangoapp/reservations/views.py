from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages
from django.core.mail import send_mail
from reservations.forms import ReservationForm
from football_fields.models import FootballField
from .models import Reservation
from datetime import datetime, timedelta

# Create your views here.


@login_required(redirect_field_name="account_login")
def create_reservation(request: HttpRequest, pk: int):
    try:
        field = FootballField.objects.get(pk=pk)
    except FootballField.DoesNotExist:
        messages.warning(request, _("Este campo não existe mais."))
        return redirect("football_field_list")

    if request.method == "POST":
        # data comes from post as str, we need to convert it to datetime if
        # we want to make operations
        start_time = datetime.strptime(request.POST.get("start_time"), "%H:%M")
        end_time = datetime.strptime(request.POST.get("end_time"), "%H:%M")

        diff_time = end_time - start_time
        total_cost = (diff_time.seconds / 60 / 60) * field.hour_price

        reservation = Reservation(
            user=request.user, football_field=field, total_cost=total_cost
        )
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            data: Reservation = form.save()
            print(data)
            messages.success(request, _("Reservation created successfully."))
            send_mail(
                subject=_("Your reservation was created."),
                message=_(
                    f"Your reservation for {data.football_field} at {data.reservation_day}, was created successfully. You will be charged {data.total_cost}."
                ),
                from_email="shacayou@gmail.com",
                recipient_list=[request.user.email],
                fail_silently=False,
            )
            return redirect(to="football_field_detail", pk=pk)
        else:
            print(form.errors)
            for error in form.errors:
                print(error)
                print(form.errors[error])

                messages.warning(request, form.errors[error])

    template_name = "reservations/create.html"
    form = ReservationForm()
    context = {"form": form, "field": field}
    return render(request, template_name=template_name, context=context)


@login_required(redirect_field_name="account_login")
def detail_reservation(request: HttpRequest, pk: int):
    context = {}
    return render(request, "reservations/detail_reservation.html", context=context)


@login_required(redirect_field_name="account_login")
def user_reservations(request: HttpRequest):
    reservations = Reservation.objects.filter(user=request.user)
    context = {"reservations": reservations}
    return render(request, "reservations/user_reservations.html", context=context)


@login_required(redirect_field_name="account_login")
def cancel_reservation(request: HttpRequest, pk: int):
    if request.method == "POST":
        try:
            reservation = Reservation.objects.get(pk=pk)
            reservation.status = "canceled"
            reservation.save()
        except Reservation.DoesNotExist:
            messages.warning(_("This reservation does not exists."))
    return redirect(to="user_reservations")
