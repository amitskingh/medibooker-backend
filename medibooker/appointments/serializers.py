from rest_framework import serializers
from .models import Appointment
from slots.serializers import SlotSerializer
from accounts.serializers import UserSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    slot = SlotSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "doctor",
            "slot",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_patient(self, obj):
        return UserSerializer(obj.patient.user).data

    def get_doctor(self, obj):
        return UserSerializer(obj.doctor.user).data
