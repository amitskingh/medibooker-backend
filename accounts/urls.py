from django.urls import path
from .views import (
    DoctorRegisterView,
    PatientRegisterView,
    EmailLoginView,
    SpecializationListView,
    DoctorListView,
    UserProfile,
    PatientListView,
)

urlpatterns = [
    path("login/", EmailLoginView.as_view()),
    # Registration
    path("doctor/register/", DoctorRegisterView.as_view()),
    path("patient/register/", PatientRegisterView.as_view()),
    # Lists
    path("specializations/", SpecializationListView.as_view()),
    path("doctors/", DoctorListView.as_view(), name="doctor-list"),
    path("patients/", PatientListView.as_view(), name="patient-list"),
    # Profile
    path("profile/", UserProfile.as_view()),
]
