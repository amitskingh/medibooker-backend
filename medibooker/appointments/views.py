from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from utils.response import success_response, error_response
from accounts.permissions import IsPatient, IsDoctor, IsAdmin
from accounts.models import Patient, Doctor
from slots.models import Slot
from .models import Appointment
from .serializers import AppointmentSerializer


class PatientBookAppointmentView(APIView):
    permission_classes = [IsPatient]

    def post(self, request):
        patient = request.user.patient_profile
        slot_id = request.data.get("slot_id")

        if not slot_id:
            return error_response("slot_id is required")

        slot = get_object_or_404(Slot, id=slot_id)

        # Ensure slot not already booked
        if slot.is_booked:
            return error_response("This slot is already booked", status=400)

        doctor = slot.doctor

        # Optional: prevent duplicate appointment for same slot & patient
        existing = Appointment.objects.filter(patient=patient, slot=slot).exists()
        if existing:
            return error_response("You already booked this slot", status=400)

        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            slot=slot,
            status="BOOKED",
        )

        # Mark slot as booked
        slot.is_booked = True
        slot.save()

        serializer = AppointmentSerializer(appointment)
        return success_response(
            "Appointment booked successfully", serializer.data, status=201
        )


class PatientAppointmentsListView(APIView):
    permission_classes = [IsPatient]

    def get(self, request):
        patient = request.user.patient_profile
        appointments = (
            Appointment.objects.filter(patient=patient)
            .select_related("doctor__user", "patient__user", "slot")
            .order_by("-created_at")
        )

        serializer = AppointmentSerializer(appointments, many=True)
        return success_response("Your appointments fetched", serializer.data)


class DoctorAppointmentsListView(APIView):
    permission_classes = [IsDoctor]

    def get(self, request):
        doctor = request.user.doctor_profile
        appointments = (
            Appointment.objects.filter(doctor=doctor)
            .select_related("doctor__user", "patient__user", "slot")
            .order_by("-created_at")
        )

        serializer = AppointmentSerializer(appointments, many=True)
        return success_response("Your appointments fetched", serializer.data)


class DoctorUpdateAppointmentStatusView(APIView):
    permission_classes = [IsDoctor]

    def patch(self, request, appointment_id):
        doctor = request.user.doctor_profile
        appointment = get_object_or_404(Appointment, id=appointment_id)

        # Ensure this appointment belongs to the doctor
        if appointment.doctor != doctor:
            return error_response(
                "You are not allowed to update this appointment", status=403
            )

        new_status = request.data.get("status")

        if new_status not in dict(Appointment.STATUS_CHOICES):
            return error_response("Invalid status", status=400)

        # Optional: you can restrict transitions
        # e.g., only BOOKED -> VISITED allowed
        if appointment.status == "VISITED" and new_status == "BOOKED":
            return error_response("Cannot revert from VISITED to BOOKED", status=400)

        appointment.status = new_status
        appointment.save()

        serializer = AppointmentSerializer(appointment)
        return success_response("Appointment status updated", serializer.data)


class AdminAppointmentsOverviewView(APIView):
    # permission_classes = [IsAdmin]

    def get(self, request):
        appointments = (
            Appointment.objects.all()
            .select_related("doctor__user", "patient__user", "slot")
            .order_by("-created_at")
        )

        serializer = AppointmentSerializer(appointments, many=True)
        return success_response("All appointments fetched", serializer.data)
