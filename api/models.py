from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom: User Model extending Django's AbstractUser, with roles for doctor and patient.
class User(AbstractUser):
    ROLES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    role = models.CharField(max_length=10, choices=ROLES)

    def __str__(self):
        return f"{self.username} ({self.role})"


# Doctor: Profile Stores additional information specific to doctors, such as specialty and bio.
class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialty = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialty}"

# Patient: Profile Stores additional information specific to patients.
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    date_of_birth = models.DateField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# Appointment: Represents an appointment between a doctor and a patient, with status tracking.
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments_as_doctor")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments_as_patient")
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment: {self.patient.username} with {self.doctor.username} on {self.date}"


# Prescription: Records prescriptions issued for an appointment.
class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="prescription")
    medicine_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.appointment.patient.username}"
