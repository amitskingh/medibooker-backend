import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models

from .managers import UserManager

# -------------------------
# Custom User Model
# -------------------------

def user_profile_upload_path(instance, filename):
    # This function defines the upload path for user profile images
    return f"profiles/user_{instance.id}/{filename}"

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ROLE_CHOICES = (
        ("doctor", "Doctor"),
        ("patient", "Patient"),
        ("admin", "Admin"),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    profile_url = models.ImageField(upload_to=user_profile_upload_path, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # only requires email + password

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


# -------------------------
# Doctor Profile
# -------------------------
class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    SPECIALIZATION_CHOICES = [
        ("cardiology", "Cardiology"),
        ("dermatology", "Dermatology"),
        ("orthopedics", "Orthopedics"),
        ("neurology", "Neurology"),
        ("pediatrics", "Pediatrics"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)

    def __str__(self):
        return f"{self.user.full_name} - {self.specialization}"


# -------------------------
# Patient Profile
# -------------------------
class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Patient: {self.user.email}"
