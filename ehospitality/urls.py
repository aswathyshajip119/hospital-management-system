"""
URL configuration for ehospitality project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from adminpanel.views import admin_login, user_management, admin_dashboard, patient_detail, delete_patient, \
    edit_patient, doctor_detail, delete_doctor, edit_doctor, appointment_management, edit_appointment, \
    delete_appointment, facility_management, edit_facility, logout_adminpanel
from patient.views import register_patient, patient_login, book_appointment, patient_dashboard, logout_patient, \
    patient_prescriptions,cancel_appointment,patient_reports,home
from doctor.views import doctor_login, doctor_dashboard, doctor_consult, logout_doctor

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_patient),
    path('login/', patient_login),
    path('book/', book_appointment),
    path('dashboard/', patient_dashboard),
    path('logout/', logout_patient),
    path('prescriptions/', patient_prescriptions),
    path('cancel/<int:appointment_id>/', cancel_appointment),
    path('reports/', patient_reports, name='reports'),
    path('doctor/login/', doctor_login, name='doctor_login'),
    path('doctor/dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('doctor/consult/<int:appointment_id>/',doctor_consult,name='doctor_consult'),
    path('adminpanel/login/', admin_login, name='adminpanel_login'),
    path('adminpanel/login/', admin_login, name='admin_login'),
    path('adminpanel/dashboard/',admin_dashboard,name='admin_dashboard'),
    path('adminpanel/users/', user_management, name='user_management'),
    path('adminpanel/patient/<int:patient_id>/',patient_detail,name='patient_detail'),
    path('adminpanel/patient/delete/<int:patient_id>/',delete_patient,name='delete_patient'),
    path('adminpanel/patient/edit/<int:patient_id>/',edit_patient,name='edit_patient'),
    path('adminpanel/doctor/<int:doctor_id>/',doctor_detail,name='doctor_detail'),
    path('adminpanel/doctor/delete/<int:doctor_id>/',delete_doctor,name='delete_doctor'),
    path('adminpanel/doctor/edit/<int:doctor_id>/',edit_doctor,name='edit_doctor'),
    path('adminpanel/appointments/',appointment_management,name='appointment_management'),
    path('adminpanel/appointment/edit/<int:appointment_id>/',edit_appointment,name='edit_appointment'),
    path('adminpanel/appointment/delete/<int:appointment_id>/',delete_appointment,name='delete_appointment'),
    path('adminpanel/facility/',facility_management,name='facility_management'),
    path('adminpanel/facility/edit/<int:doctor_id>/',edit_facility,name='edit_facility'),
    path('doctor/logout/', logout_doctor, name='logout_doctor'),
    path('adminpanel/logout/',logout_adminpanel,name='admin_logout'),
]
