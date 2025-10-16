# HospitalManagementAPI
A RESTful API built with Django REST Framework for managing hospital operations, including patients, doctors, appointments, and  prescriptions. This API is designed to make hospital workflows easier, scalable, and secure. Supports user registration, JWT authentication, and role-based access control.


1. Technology Stack

Python: 3.10.11

Django: 5.2.7

Django REST Framework: 3.16.1

JWT Authentication: djangorestframework-simplejwt 5.5.1

Database: SQLite (default)



---

2. Installation & Setup

Step 1: Clone the repository

git clone <your-repo-url>
cd hospital_management_api

Step 2: Create a virtual environment

python -m venv venv

Step 3: Activate the virtual environment

Windows:


venv\Scripts\activate

macOS/Linux:


source venv/bin/activate

Step 4: Install dependencies

pip install -r requirements.txt

Step 5: Apply migrations

python manage.py migrate

Step 6: Create a superuser (optional)

python manage.py createsuperuser

Step 7: Run the development server

python manage.py runserver


---

3. Authentication

Users must register via /api/register/

JWT authentication is used for secure endpoints

Obtain JWT token: POST /api/token/

Refresh token: POST /api/token/refresh/



---

4. API Endpoints Overview

Endpoint	Method	Description	Permissions

/api/register/	POST	Register a new user (doctor or patient)	AllowAny
/api/doctors/	GET	List all doctors	Authenticated
/api/doctors/int:pk/	GET, PUT	Retrieve or update doctor profile	Authenticated, Doctor owns profile
/api/doctors/available/	GET	List available doctors for appointment selection	Authenticated, Patient
/api/patients/	GET	List all patients	Authenticated
/api/patients/int:pk/	GET, PUT	Retrieve or update patient profile	Authenticated, Patient owns profile
/api/appointments/request/	POST	Patient requests a new appointment	Authenticated, Patient
/api/appointments/	GET	List appointments relevant to logged-in user	Authenticated
/api/appointments/int:pk/update/	PUT	Update appointment status (confirmed, cancelled, completed)	Authenticated, Doctor
/api/prescriptions/	GET	List prescriptions (doctors see theirs, patients see theirs)	Authenticated
/api/prescriptions/create/	POST	Create a prescription for an appointment	Authenticated, Doctor
/api/token/	POST	Obtain JWT access and refresh tokens	AllowAny
/api/token/refresh/	POST	Refresh JWT access token	AllowAny



---

5. Roles & Permissions

Doctor

View and update own profile

Manage own appointments

Create prescriptions for their appointments


Patient

View and update own profile

Request appointments

View own prescriptions



---

6. Example Requests

Register a User

POST /api/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "strongpassword",
  "role": "patient"
}

Obtain JWT Token

POST /api/token/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "strongpassword"
}

Refresh JWT Token

POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}

Request an Appointment (Patient)

POST /api/appointments/request/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "doctor": 1,
  "notes": "Need consultation for headache"
}

List Appointments

GET /api/appointments/
Authorization: Bearer <access_token>

Update Appointment Status (Doctor)

PUT /api/appointments/1/update/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "confirmed",
  "date": "2025-10-20",
  "time": "14:00"
}

Create a Prescription (Doctor)

POST /api/prescriptions/create/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "appointment": 1,
  "medicine_name": "Paracetamol",
  "dosage": "500mg",
  "instructions": "Take twice daily after meals"
}


---

7. Project Structure

HospitalManagementAPI/
│
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── filters.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── HospitalManagementAPI/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── staticfiles/
│   └── (auto-collected static files)
│
├── templates/
│   └── (HTML templates if any)
│
├── manage.py
├── Procfile
├── requirements.txt
├── runtime.txt
├── .env
├── .gitignore
└── README.md

8. Notes

Database is SQLite by default; can be changed in settings.py

JWT access tokens expire after 60 minutes; refresh tokens valid for 1 day

Custom user model User is used (AUTH_USER_MODEL = "api.User")

Timezone: Africa/Lagos

Ensure virtual environment is activated before running migrations or server



---

9. Quick Start Summary

1. Clone repository and setup virtual environment


2. Install dependencies


3. Apply migrations


4. Create a superuser (optional)


5. Run development server


6. Use API endpoints with JWT authentication



