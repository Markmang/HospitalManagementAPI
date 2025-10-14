from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # USER REGISTRATION Endpoint
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),

    # DOCTOR PROFILE Endpoints
    path('doctors/', views.DoctorProfileListView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', views.DoctorProfileDetailView.as_view(), name='doctor-detail'),

    # PATIENT PROFILE Endpoints
    path('patients/', views.PatientProfileListView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', views.PatientProfileDetailView.as_view(), name='patient-detail'),
    path('doctors/available/', views.AvailableDoctorsView.as_view(), name='available-doctors'),


    # APPOINTMENTS Endpoints
    path('appointments/request/', views.AppointmentRequestView.as_view(), name='appointment-request'),
    path('appointments/', views.AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/update/', views.AppointmentUpdateView.as_view(), name='appointment-update'),

    # PRESCRIPTIONS Endpoints
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescription-list'),
    path('prescriptions/create/', views.PrescriptionCreateView.as_view(), name='prescription-create'),
    # JWT Authentication Endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
