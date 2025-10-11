from rest_framework import serializers
from .models import User, DoctorProfile, PatientProfile, Appointment, Prescription


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Create user with hashed password."""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user



# Doctor Profile Serializer
class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = ['id', 'user', 'specialty', 'bio']


# Patient Profile Serializer
class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = ['id', 'user', 'date_of_birth', 'medical_history']


# Appointment Serializer 
class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()
    patient = serializers.StringRelatedField()

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'date', 'time', 'status', 'notes']


# Prescription Serializer 
class PrescriptionSerializer(serializers.ModelSerializer):
    appointment = serializers.StringRelatedField()

    class Meta:
        model = Prescription
        fields = ['id', 'appointment', 'medicine_name', 'dosage', 'instructions', 'issued_at']
