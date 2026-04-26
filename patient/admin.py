from django.contrib import admin
from .models import Patient,Appointment,Prescription, Report

admin.site.register(Appointment)

admin.site.register(Patient)

admin.site.register(Prescription)

admin.site.register(Report)