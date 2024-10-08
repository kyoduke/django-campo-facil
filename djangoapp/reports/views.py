import csv
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reservations.models import Reservation
from reports.forms import FootballFieldReportFilterForm


@login_required(redirect_field_name="account_login")
def index(request: HttpRequest):
    if not request.user.is_staff:
        return HttpResponse(_("Page not found"))
    if request.GET:
        form = FootballFieldReportFilterForm(request.GET)
    else:
        form = FootballFieldReportFilterForm()

    context = {"form": form}

    return render(request, "reports/index.html", context=context)


@login_required(redirect_field_name="account_login")
def csv_report(request: HttpRequest):
    if not request.user.is_staff:
        return HttpResponse(_("Page not found"))
    form = FootballFieldReportFilterForm(request.GET or None)
    reservations = Reservation.objects.all()
    if form.is_valid():
        from_date = form.cleaned_data["from_date"] or None
        to_date = form.cleaned_data["to_date"] or None
        if from_date:
            reservations = reservations.filter(
                reservation_day__gt=form.cleaned_data["from_date"]
            )
        if to_date:
            reservations = reservations.filter(
                reservation_day__lt=form.cleaned_data["to_date"]
            )

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="report.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(
        [
            "football_field",
            "state",
            "city",
            "district",
            "user",
            "first_name",
            "last_name",
            "date",
            "start_time",
            "end_time",
            "total_cost",
        ]
    )
    for reservation in reservations:
        writer.writerow(
            [
                reservation.football_field.name,
                reservation.football_field.address.state,
                reservation.football_field.address.city,
                reservation.football_field.address.district,
                reservation.user.email,
                reservation.user.first_name,
                reservation.user.last_name,
                reservation.reservation_day,
                reservation.start_time,
                reservation.end_time,
                reservation.total_cost,
            ]
        )
    return response


@login_required(redirect_field_name="account_login")
def pdf_report(request: HttpRequest):
    if not request.user.is_staff:
        return HttpResponse(_("Page not found"))
    form = FootballFieldReportFilterForm(request.GET or None)
    reservations = Reservation.objects.all()
    if form.is_valid():
        from_date = form.cleaned_data["from_date"] or None
        to_date = form.cleaned_data["to_date"] or None
        if from_date:
            reservations = reservations.filter(
                reservation_day__gte=form.cleaned_data["from_date"]
            )
        if to_date:
            reservations = reservations.filter(
                reservation_day__lte=form.cleaned_data["to_date"]
            )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=report.pdf"

    c = canvas.Canvas(response, pagesize=letter)
    c.setTitle("Reservations Report")
    headers = [
        "ID",
        _("Football Field"),
        _("State"),
        _("User"),
        _("Date"),
        _("Start Time"),
        _("End Time"),
        _("Cost"),
        _("Status"),
    ]
    data = [headers]
    for reservation in reservations:
        data.append(
            [
                reservation.pk,
                reservation.football_field.name,
                reservation.football_field.address.state,
                reservation.user.email,
                reservation.reservation_day,
                str(reservation.start_time)[0:5],
                str(reservation.end_time)[0:5],
                reservation.total_cost,
                reservation.status,
            ]
        )

    table = Table(data)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ]
        )
    )
    table.wrapOn(c, 600, 600)
    table.drawOn(c, 40, 600 - len(data))
    c.save()

    return response
