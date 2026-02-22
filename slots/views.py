from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from accounts.permissions import IsDoctor, IsPatient
from rest_framework import status
from utils.response import success_response, error_response
from .models import Slot
from accounts.models import Doctor
from .serializers import SlotSerializer


class DoctorSlotsView(APIView):
    permission_classes = [IsDoctor]

    def get(self, request):
        doctor = request.user.doctor_profile
        slots = Slot.objects.filter(doctor=doctor).order_by("date", "start_time")
        serializer = SlotSerializer(slots, many=True)
        return success_response("Your slots fetched", serializer.data)

    def post(self, request):
        doctor = request.user.doctor_profile
        serializer = SlotSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response("Validation error", serializer.errors)

        date = serializer.validated_data["date"]
        start = serializer.validated_data["start_time"]
        end = serializer.validated_data["end_time"]

        # Duplicate slot check
        if Slot.objects.filter(
            doctor=doctor, date=date, start_time=start, end_time=end
        ).exists():
            return error_response("This exact slot already exists for the doctor.")

        # Overlap check
        if Slot.objects.filter(
            doctor=doctor, date=date, start_time__lt=end, end_time__gt=start
        ).exists():
            return error_response("This slot overlaps with an existing one.")

        # Save
        serializer.save(doctor=doctor)
        return success_response("Slot created successfully", serializer.data, 201)


class DoctorSlotDetailView(APIView):
    permission_classes = [IsDoctor]

    def delete(self, request, slot_id):
        doctor = request.user.doctor_profile
        slot = get_object_or_404(Slot, id=slot_id)

        # Ensure the slot belongs to the doctor
        if slot.doctor != doctor:
            return error_response(
                "You are not allowed to delete this slot.",
                status=status.HTTP_403_FORBIDDEN,
            )

        # Prevent deleting a booked slot
        if slot.is_booked:
            return error_response(
                "Cannot delete a slot that is already booked.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        slot.delete()
        return success_response(
            "Slot deleted successfully", status=status.HTTP_204_NO_CONTENT
        )


class SlotsListView(APIView):
    def get(self, request):
        doctor_id = request.GET.get("doctor")
        date = request.GET.get("date")
        print("NO ID: ", doctor_id)

        if not doctor_id:
            return error_response("Doctor id is required")

        # Ensure doctor exists
        if not Doctor.objects.filter(id=doctor_id).exists():
            return error_response("Invalid doctor id")

        qs = Slot.objects.filter(doctor_id=doctor_id, is_booked=False)

        if date:
            qs = qs.filter(date=date)

        qs = qs.order_by("date", "start_time")

        serializer = SlotSerializer(qs, many=True)
        print(serializer.data)
        return success_response("Available slots fetched", serializer.data, 200)
