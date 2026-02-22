from django.urls import path
from .views import (
    PatientBookAppointmentView,
    PatientAppointmentsListView,
    DoctorAppointmentsListView,
    DoctorUpdateAppointmentStatusView,
    AdminAppointmentsOverviewView,
)

urlpatterns = [
    path("book/", PatientBookAppointmentView.as_view()),  # POST: create appointment
    # Patient-specific appointments
    path("patient/", PatientAppointmentsListView.as_view()),
    # Doctor-specific appointments
    path("doctor/", DoctorAppointmentsListView.as_view()),
    # Doctor updates appointment status (accepted, rejected, completed)
    path("<int:appointment_id>/status/", DoctorUpdateAppointmentStatusView.as_view()),
    # Admin: view all appointments
    path("admin/", AdminAppointmentsOverviewView.as_view()),
]
