from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages
from django.core.mail import send_mail
from reservations.forms import ReservationForm
from football_fields.models import FootballField
from .models import Reservation
from datetime import datetime
from django.conf import settings

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
                    f"Your reservation for the football field {data.football_field} on {data.reservation_day} has been successfully created. The total cost for your reservation is {data.total_cost}. Thank you for choosing our service!"
                ),
                from_email=getattr(settings, "EMAIL_HOST_USER", None),
                recipient_list=[request.user.email],
                fail_silently=False,
            )
            send_mail(
                subject=_("Your field have a new reservation."),
                message=_(
                    f"There is a new reservation for {reservation.football_field.name}.\nThe reservation is set to {reservation.reservation_day} from {reservation.start_time} to {reservation.end_time}.\nReservation Details\nUser: {reservation.user.get_full_name()}\nEmail: {reservation.user.email}\nTotal Cost: R$ {reservation.total_cost}"
                ),
                from_email=getattr(settings, "EMAIL_HOST_USER", None),
                recipient_list=[reservation.football_field.owner.email],
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
    reservations = Reservation.objects.filter(user=request.user, is_active=True)
    context = {"reservations": reservations}
    return render(request, "reservations/user_reservations.html", context=context)


@login_required(redirect_field_name="account_login")
def cancel_reservation(request: HttpRequest, pk: int):
    if request.method == "POST":
        try:
            reservation = Reservation.objects.get(pk=pk)
            reservation.status = "canceled"
            reservation.save()
            send_mail(
                subject=_("Reservation have been canceled."),
                message=f"A reservation have been canceled for {reservation.football_field.name} on {reservation.reservation_day}.",
                from_email=getattr(settings, "EMAIL_HOST_USER", None),
                recipient_list=[reservation.football_field.owner],
                fail_silently=False,
            )
        except Reservation.DoesNotExist:
            messages.warning(_("This reservation does not exists."))
    return redirect(to="user_reservations")


@login_required(redirect_field_name="account_login")
def remove_reservation(request: HttpRequest, pk: int):
    if request.method == "POST":
        try:
            reservation = Reservation.objects.get(pk=pk)
            reservation.is_active = False
            reservation.save()
        except Reservation.DoesNotExist:
            messages.warning(_("This reservation does not exists."))
    return redirect(to="user_reservations")
