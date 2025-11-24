from django.urls import path
from .views import DoctorSlotsView, SlotsListView

urlpatterns = [
    path(
        "", DoctorSlotsView.as_view(), name="doctor-slots"
    ),  # GET + POST: /api/v1/slots/
    path("available/", SlotsListView.as_view(), name="available-slots"),
]
