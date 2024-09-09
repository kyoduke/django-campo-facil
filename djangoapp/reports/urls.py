from django.urls import path
from reports import views

urlpatterns = [
    path("", views.index, name="reports_index"),
    path("csv/", views.csv_report, name="csv_report"),
    path("pdf/", views.pdf_report, name="pdf_report"),
]
