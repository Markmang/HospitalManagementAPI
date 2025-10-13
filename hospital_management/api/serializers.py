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
        """Create user with hashed password and auto profile based on role."""
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)

        user = User(**validated_data)
        if password:
            user.set_password(password)
        if role:
            user.role = role
        user.save()

        # Automatically create related profile
        if role == 'doctor':
            DoctorProfile.objects.create(user=user)
        elif role == 'patient':
            PatientProfile.objects.create(user=user)

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
    doctor = serializers.StringRelatedField(read_only=True)
    patient = serializers.StringRelatedField(read_only=True)

    # Allow flexible date/time input formats
    date = serializers.DateField(input_formats=['%Y-%m-%d', '%m/%d/%Y'])
    time = serializers.TimeField(input_formats=['%H:%M', '%H:%M:%S', '%I:%M %p'])

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'date', 'time', 'status', 'notes']
        read_only_fields = ['status']  # Prevent patients from changing status

# Prescription Serializer 
class PrescriptionSerializer(serializers.ModelSerializer):
    appointment = serializers.StringRelatedField()

    class Meta:
        model = Prescription
        fields = ['id', 'appointment', 'medicine_name', 'dosage', 'instructions', 'issued_at']

# Serializer for creating appointments (patients only)
class AppointmentCreateSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=DoctorProfile.objects.all())

    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'notes']  # no status or patient — handled automatically
