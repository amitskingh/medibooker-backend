from django.urls import path
from .views import DoctorSlotsView, SlotsListView, DoctorSlotDetailView

urlpatterns = [
    path(
        "", DoctorSlotsView.as_view(), name="doctor-slots"
    ),  # GET + POST: /api/v1/slots/
    path("available/", SlotsListView.as_view(), name="available-slots"),
    path("<int:slot_id>/", DoctorSlotDetailView.as_view(), name="doctor-slot-detail"),
]
