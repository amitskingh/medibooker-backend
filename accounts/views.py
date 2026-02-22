from rest_framework.views import APIView
from utils.response import success_response, error_response
from .serializers import (
    DoctorRegisterSerializer,
    PatientRegisterSerializer,
    PatientSerializer,
    UserSerializer,
)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Doctor, Patient
from .permissions import IsPatient, IsAdmin
from .serializers import DoctorSerializer
from rest_framework.permissions import IsAuthenticated


class DoctorRegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = DoctorRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Validation error", serializer.errors, 400)

        serializer.save()
        return success_response("Doctor registered successfully", None, 201)


class DoctorListView(APIView):
    permission_classes = [IsPatient | IsAdmin]

    def get(self, request):
        specialization = request.GET.get("specialization")

        qs = Doctor.objects.select_related("user").all()

        if specialization:
            qs = qs.filter(specialization=specialization)

        serializer = DoctorSerializer(qs, many=True)
        return success_response("Doctors fetched", serializer.data)


class PatientListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        qs = Patient.objects.select_related("user").all()
        serializer = PatientSerializer(qs, many=True)
        return success_response("Patients fetched", serializer.data)


class SpecializationListView(APIView):
    permission_classes = []

    def get(self, request):
        specializations = [
            {"key": key, "value": value} for key, value in Doctor.SPECIALIZATION_CHOICES
        ]
        return success_response("Specializations fetched", specializations)


class PatientRegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PatientRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Validation error", serializer.errors, 400)

        serializer.save()
        return success_response("Patient registered successfully", None, 201)


class EmailLoginView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return error_response("Email and password required")

        user = authenticate(request, email=email, password=password)
        if user is None:
            return error_response("Invalid email or password", status=401)

        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
        }

        return success_response("Login successful", data, 200)


class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == "doctor":
            try:
                serializer = DoctorSerializer(user.doctor_profile)
                return success_response("Doctor profile fetched", serializer.data)
            except Doctor.DoesNotExist:
                return error_response("Doctor profile not found", status=404)
        elif user.role == "patient":
            try:
                serializer = PatientSerializer(user.patient_profile)
                return success_response("Patient profile fetched", serializer.data)
            except Patient.DoesNotExist:
                return error_response("Patient profile not found", status=404)

        serializer = UserSerializer(user)
        return success_response("User profile fetched", serializer.data)
