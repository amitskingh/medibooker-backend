from django.db import models
from accounts.models import Doctor, Patient
from slots.models import Slot


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("BOOKED", "Booked"),
        ("VISITED", "Visited"),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointments"
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="appointments"
    )
    slot = models.OneToOneField(
        Slot, on_delete=models.CASCADE, related_name="appointment"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="BOOKED")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment #{self.id} - {self.patient.user.full_name} with {self.doctor.user.full_name}"
