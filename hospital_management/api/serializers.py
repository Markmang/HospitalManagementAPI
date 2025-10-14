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
        read_only_fields = ['doctor', 'patient', 'notes']  # doctors can’t change patient's notes

    def __init__(self, *args, **kwargs):
        """Customize fields dynamically based on user role."""
        super().__init__(*args, **kwargs)
        request = self.context.get('request')

        if request:
            if request.user.role == 'patient':
                # Patients can only set date, time, and notes (status handled automatically)
                self.fields['status'].read_only = True
            elif request.user.role == 'doctor':
                # Doctors can’t edit notes (only date/time/status)
                self.fields['notes'].read_only = True

# Prescription Serializer 
class PrescriptionSerializer(serializers.ModelSerializer):
    appointment = serializers.PrimaryKeyRelatedField(
        queryset=Appointment.objects.none(),  # default empty until set in __init__
        write_only=True
    )
    doctor = serializers.CharField(source='appointment.doctor.username', read_only=True)
    patient = serializers.CharField(source='appointment.patient.username', read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'id',
            'appointment',
            'doctor',
            'patient',
            'medicine_name',
            'dosage',
            'instructions',
            'issued_at',
        ]
        read_only_fields = ['issued_at', 'doctor', 'patient']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            # If the logged-in user is a doctor, show only their appointments
            if request.user.role == 'doctor':
                self.fields['appointment'].queryset = Appointment.objects.filter(doctor=request.user)


# Serializer for creating appointments (patients only)
class AppointmentCreateSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=DoctorProfile.objects.all())

    class Meta:
        model = Appointment
        fields = ['doctor', 'notes']  # no status or patient — handled automatically
