from rest_framework import serializers
from .models import User, Doctor, Patient
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ["id", "email", "first_name", "last_name", "full_name", "role"]

    def get_full_name(self, obj):
        return obj.full_name


class DoctorSerializer(serializers.ModelSerializer):
    specialization_display = serializers.CharField(
        source="get_specialization_display", read_only=True
    )

    user = UserSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = ["id", "specialization", "specialization_display", "user"]


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ["id", "phone_number", "user"]


class DoctorRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    specialization = serializers.CharField()

    def validate_specialization(self, value):
        value = value.lower().strip()
        valid_choices = [choice[0] for choice in Doctor.SPECIALIZATION_CHOICES]

        if value not in valid_choices:
            raise serializers.ValidationError(
                f"Invalid specialization. Allowed: {valid_choices}"
            )
        return value

    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            role="doctor",
        )

        Doctor.objects.create(
            user=user, specialization=validated_data["specialization"]
        )

        return user


class PatientRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()

    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            role="patient",
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        Patient.objects.create(user=user, phone_number=validated_data["phone_number"])

        return user
