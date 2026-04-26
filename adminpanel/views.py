from django.shortcuts import render, redirect, get_object_or_404
from datetime import date

from patient.models import Patient, Appointment, Prescription, Report
from doctor.models import Doctor




def admin_login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "adminpanel" and password == "admin123":

            request.session['admin_logged_in'] = True
            request.session['admin_name'] = "Administrator"

            return redirect('/adminpanel/dashboard/')

        else:
            return render(request, 'adminpanel/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'adminpanel/login.html')


def user_management(request):

    if not request.session.get('admin_logged_in'):
        return redirect('/adminpanel/login/')

    patients = Patient.objects.all().order_by('id')
    doctors = Doctor.objects.all().order_by('id')

    return render(request, 'adminpanel/user_management.html', {
        'patients': patients,
        'doctors': doctors
    })

def admin_dashboard(request):

    if not request.session.get('admin_logged_in'):
        return redirect('/adminpanel/login/')

    today = date.today()

    total_patients = Patient.objects.count()

    total_doctors = Doctor.objects.count()

    today_appointments = Appointment.objects.filter(
        date=today
    ).count()

    completed_today = Appointment.objects.filter(
        date=today,
        status="Completed"
    ).count()

    return render(request, 'adminpanel/dashboard.html', {
        'admin_name': request.session.get(
            'admin_name',
            'Administrator'
        ),
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'today_appointments': today_appointments,
        'completed_today': completed_today
    })

def patient_detail(request, patient_id):

    if not request.session.get('admin_logged_in'):
        return redirect('/adminpanel/login/')

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by('-date')

    prescriptions = Prescription.objects.filter(
        patient=patient
    ).order_by('-date')

    reports = Report.objects.filter(
        patient=patient
    ).order_by('-date')

    return render(request, 'adminpanel/patient_detail.html', {
        'patient': patient,
        'appointments': appointments,
        'prescriptions': prescriptions,
        'reports': reports
    })

def delete_patient(request, patient_id):

    if not request.session.get('admin_logged_in'):
        return redirect('/adminpanel/login/')

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    patient.delete()

    return redirect('/adminpanel/users/')

def edit_patient(request, patient_id):

    if not request.session.get('admin_logged_in'):
        return redirect('/adminpanel/login/')

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    if request.method == "POST":

        patient.name = request.POST.get('name')
        patient.email = request.POST.get('email')
        patient.phone = request.POST.get('phone')
        patient.age = request.POST.get('age')
        patient.gender = request.POST.get('gender')

        patient.save()

        return redirect(f'/adminpanel/patient/{patient.id}/')

    return render(request, 'adminpanel/edit_patient.html', {
        'patient': patient
    })

def doctor_detail(request, doctor_id):

    if not request.session.get('admin_logged_in'):
        return redirect('/adminpanel/login/')

    doctor = get_object_or_404(
        Doctor,
        id=doctor_id
    )

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).order_by('-date')

    return render(request, 'adminpanel/doctor_detail.html', {
        'doctor': doctor,
        'appointments': appointments
    })

def delete_doctor(request, doctor_id):

    if not request.session.get('admin_logged_in'):
        return redirect('/adminpanel/login/')

    doctor = get_object_or_404(
        Doctor,
        id=doctor_id
    )

    doctor.delete()

    return redirect('/adminpanel/users/')

def edit_doctor(request, doctor_id):

    if not request.session.get('admin_logged_in'):
        return redirect('/adminpanel/login/')

    doctor = get_object_or_404(
        Doctor,
        id=doctor_id
    )

    if request.method == "POST":

        doctor.name = request.POST.get('name')
        doctor.email = request.POST.get('email')
        doctor.phone = request.POST.get('phone')
        doctor.specialization = request.POST.get('specialization')

        doctor.save()

        return redirect(f'/adminpanel/doctor/{doctor.id}/')

    return render(request, 'adminpanel/edit_doctor.html', {
        'doctor': doctor
    })

def appointment_management(request):

    if not request.session.get('admin_logged_in'):
        return redirect('/adminpanel/login/')

    appointments = Appointment.objects.all().order_by('-date', '-id')

    return render(request, 'adminpanel/appointments.html', {
        'appointments': appointments
    })




def edit_appointment(request, appointment_id):

    if not request.session.get('admin_logged_in'):
        return redirect('/adminpanel/login/')

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    doctors = Doctor.objects.all()

    if request.method == "POST":

        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')

        appointment.doctor = Doctor.objects.get(id=doctor_id)
        appointment.date = date

        appointment.save()

        return redirect('/adminpanel/appointments/')

    return render(request, 'adminpanel/edit_appointment.html', {
        'appointment': appointment,
        'doctors': doctors
    })

def delete_appointment(request, appointment_id):

    if not request.session.get('admin_logged_in'):
        return redirect('/adminpanel/login/')

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    appointment.delete()

    return redirect('/adminpanel/appointments/')

def facility_management(request):

    if not request.session.get('admin_logged_in'):
        return redirect('/adminpanel/login/')

    doctors = Doctor.objects.all().order_by('id')

    return render(
        request,
        'adminpanel/facility_management.html',
        {'doctors': doctors}
    )





def edit_facility(request, doctor_id):

    if not request.session.get('admin_logged_in'):
        return redirect('/adminpanel/login/')

    doctor = get_object_or_404(
        Doctor,
        id=doctor_id
    )

    if request.method == "POST":

        doctor.op_time = request.POST.get('op_time')
        doctor.available_days = request.POST.get('available_days')

        doctor.save()

        return redirect('/adminpanel/facility/')

    return render(
        request,
        'adminpanel/edit_facility.html',
        {'doctor': doctor}
    )

def logout_adminpanel(request):
    request.session.flush()
    return redirect('/')

