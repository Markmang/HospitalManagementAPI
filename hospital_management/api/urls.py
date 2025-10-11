from django.urls import path
from . import views

urlpatterns = [
    # USER REGISTRATION
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),

    # DOCTOR PROFILE
    path('doctors/', views.DoctorProfileListView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', views.DoctorProfileDetailView.as_view(), name='doctor-detail'),

    # PATIENT PROFILE
    path('patients/', views.PatientProfileListView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', views.PatientProfileDetailView.as_view(), name='patient-detail'),

    # APPOINTMENTS
    path('appointments/request/', views.AppointmentRequestView.as_view(), name='appointment-request'),
    path('appointments/', views.AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/update/', views.AppointmentUpdateView.as_view(), name='appointment-update'),

    # PRESCRIPTIONS 
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescription-list'),
    path('prescriptions/create/', views.PrescriptionCreateView.as_view(), name='prescription-create'),
    path('prescriptions/<int:pk>/', views.PrescriptionDetailView.as_view(), name='prescription-detail'),
]
