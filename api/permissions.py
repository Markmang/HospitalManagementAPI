from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    """Allow access only to users with doctor role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'doctor'


class IsPatient(permissions.BasePermission):
    """Allow access only to users with patient role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'patient'


class IsAppointmentOwnerOrDoctor(permissions.BasePermission):
    """Allow patients to view their appointments and doctors to manage their own."""
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.patient or
            request.user == obj.doctor
        )

class IsPrescriptionOwnerOrDoctor(permissions.BasePermission):
    """
    Allows patients to view their own prescriptions,
    and doctors to view prescriptions they created.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Doctor who issued it OR patient for whom it was issued
            return (
                request.user == obj.appointment.doctor.user or
                request.user == obj.appointment.patient.user
            )
        # Only doctors can modify prescriptions
        return request.user.role == 'doctor'