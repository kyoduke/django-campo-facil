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


@login_required(redirect_field_name='account_login')
def index(request: HttpRequest):
    return render(request, 'reports/index.html')


@login_required(redirect_field_name='account_login')
def csv_report(request: HttpRequest):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="report.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['football field', 'city', 'user', 'date', 'start time', 'end time', 'paid'])
    for reservation in Reservation.objects.all():
        writer.writerow([
            reservation.football_field.name,
            reservation.football_field.address.city,
            reservation.user.email,
            reservation.reservation_day,
            reservation.start_time,
            reservation.end_time,
            reservation.total_cost,
        ])
    return response


def pdf_report(request: HttpRequest):
    reservations = Reservation.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=report.pdf'


    c = canvas.Canvas(response, pagesize=letter)
    c.setTitle('Reservations Report')
    headers = ['ID', _('Football Field'), _('City'), _('User'), _('Date'), _('Start Time'), _('End Time'), _('Cost'), _('Status')]
    data = [headers]
    for reservation in reservations:
        data.append([
            reservation.pk,
            reservation.football_field.name,
            reservation.football_field.address.city,
            reservation.user.email,
            reservation.reservation_day,
            reservation.start_time,
            reservation.end_time,
            reservation.total_cost,
            reservation.status,
        ])

    table = Table(data)
    table.setStyle(TableStyle(
        [
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]
    ))
    table.wrapOn(c, 600, 600)
    table.drawOn(c, 40, 600 - len(data))
    c.save()

    return response