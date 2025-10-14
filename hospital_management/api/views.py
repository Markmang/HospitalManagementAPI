from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers
from .models import User, DoctorProfile, PatientProfile, Appointment, Prescription
from .serializers import (
    UserSerializer,
    DoctorProfileSerializer,
    PatientProfileSerializer,
    AppointmentSerializer,
    PrescriptionSerializer,
    AppointmentCreateSerializer,
)
from .permissions import IsDoctor, IsPatient, IsAppointmentOwnerOrDoctor, IsPrescriptionOwnerOrDoctor


# -------------------- USER REGISTRATION --------------------
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# -------------------- DOCTOR PROFILE --------------------
class DoctorProfileListView(generics.ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        """Only allow doctors to view or update their own profile."""
        user = self.request.user
        if user.role == 'doctor':
            return DoctorProfile.objects.filter(user=user)
        return DoctorProfile.objects.none()



# -------------------- PATIENT PROFILE --------------------
class PatientProfileListView(generics.ListAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class PatientProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get_queryset(self):
        """Only allow patients to view or update their own profile."""
        user = self.request.user
        if user.role == 'patient':
            return PatientProfile.objects.filter(user=user)
        return PatientProfile.objects.none()

class AvailableDoctorsView(generics.ListAPIView):
    """List all doctors available for appointment selection."""
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get_queryset(self):
        return DoctorProfile.objects.all()


# -------------------- APPOINTMENT --------------------
class AppointmentRequestView(generics.CreateAPIView):
    serializer_class = AppointmentCreateSerializer
    permission_classes = [IsPatient, permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Allow only patients to request appointments (pending by default)."""
        doctor_id = self.request.data.get('doctor')
        if not doctor_id:
            raise serializers.ValidationError({"doctor": "Doctor ID is required."})

        try:
            doctor_profile = DoctorProfile.objects.get(id=doctor_id)
        except DoctorProfile.DoesNotExist:
            raise serializers.ValidationError({"doctor": "Invalid doctor ID."})

        serializer.save(
            patient=self.request.user,
            doctor=doctor_profile.user,
            status='pending'
        )


class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only appointments relevant to the logged-in user."""
        user = self.request.user
        if user.role == 'doctor':
            return Appointment.objects.filter(doctor=user).order_by('-date')
        elif user.role == 'patient':
            return Appointment.objects.filter(patient=user).order_by('-date')
        return Appointment.objects.none()


class AppointmentUpdateView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]


    def update(self, request, *args, **kwargs):
        """Allow doctor to confirm, cancel, or complete appointment."""
        appointment = self.get_object()
        status_choice = request.data.get('status')

        if status_choice not in ['confirmed', 'cancelled', 'completed']:
            return Response({"error": "Invalid status update."}, status=status.HTTP_400_BAD_REQUEST)

        # Allow doctor to set date/time when confirming
        if status_choice == 'confirmed':
            appointment.date = request.data.get('date', appointment.date)
            appointment.time = request.data.get('time', appointment.time)

        appointment.status = status_choice
        appointment.save()
        return Response(AppointmentSerializer(appointment).data)


# -------------------- PRESCRIPTION --------------------
class PrescriptionListView(generics.ListAPIView):
    """Doctors see all they issued; patients see only theirs."""
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Prescription.objects.filter(appointment__doctor=user)
        elif user.role == 'patient':
            return Prescription.objects.filter(appointment__patient=user)
        return Prescription.objects.none()


class PrescriptionCreateView(generics.CreateAPIView):
    """Only doctors can create prescriptions."""
    serializer_class = PrescriptionSerializer
    permission_classes = [IsDoctor]

    def perform_create(self, serializer):
        """Ensure doctor can only prescribe for their own appointments."""
        appointment_id = self.request.data.get('appointment')
        appointment = get_object_or_404(Appointment, id=appointment_id)

        if appointment.doctor != self.request.user:
            raise PermissionDenied("You can only prescribe for your own appointments.")

        serializer.save(appointment=appointment)


