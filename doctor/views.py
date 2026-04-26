from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from patient.models import Appointment, Prescription, Report
from doctor.models import Doctor



def doctor_login(request):

    if request.method == "POST":
        doctor_id = request.POST.get('doctor_id')
        email = request.POST.get('email')

        try:
            doctor = Doctor.objects.get(
                id=doctor_id,
                email=email
            )

            request.session['doctor_id'] = doctor.id

            return redirect('/doctor/dashboard/')

        except Doctor.DoesNotExist:
            return render(request, 'doctor/login.html', {
                'error': 'Invalid login details'
            })

    return render(request, 'doctor/login.html')

def doctor_dashboard(request):

    doctor_id = request.session.get('doctor_id')

    if not doctor_id:
        return redirect('/doctor/login/')

    doctor = Doctor.objects.get(id=doctor_id)

    today = date.today()

    appointments = Appointment.objects.filter(
        doctor=doctor,
        date=today
    ).exclude(
        status="Cancelled"
    ).order_by('id')

    appointments_left = appointments.filter(
        status="Pending"
    ).count()

    return render(request, 'doctor/dashboard.html', {
        'doctor': doctor,
        'appointments': appointments,
        'appointments_left': appointments_left
    })

def doctor_consult(request, appointment_id):

    # Check doctor login
    doctor_id = request.session.get('doctor_id')

    if not doctor_id:
        return redirect('/doctor/login/')

    doctor = get_object_or_404(
        Doctor,
        id=doctor_id
    )

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    patient = appointment.patient

    # Past history
    past_prescriptions = Prescription.objects.filter(
        patient=patient
    ).order_by('-date')

    past_reports = Report.objects.filter(
        patient=patient
    ).order_by('-date')

    # Save Prescription
    if request.method == "POST" and "save_prescription" in request.POST:

        medicine = request.POST.get('medicine')

        if medicine:
            Prescription.objects.create(
                patient=patient,
                doctor=doctor,
                medicine=medicine
            )

            appointment.status = "Completed"
            appointment.save()

        return redirect(f'/doctor/consult/{appointment.id}/')

    # Save Report
    if request.method == "POST" and "save_report" in request.POST:

        report_name = request.POST.get('report_name')
        result = request.POST.get('result')

        if report_name and result:

            Report.objects.create(
                patient=patient,
                report_name=report_name,
                result=result
            )

        return redirect(f'/doctor/consult/{appointment.id}/')
    # Mark Completed
    if request.method == "POST" and "mark_completed" in request.POST:
        appointment.status = "Completed"
        appointment.save()
        return redirect('/doctor/dashboard/')

    return render(
        request,
        'doctor/consult.html',
        {
            'doctor': doctor,
            'appointment': appointment,
            'patient': patient,
            'past_prescriptions': past_prescriptions,
            'past_reports': past_reports
        }
    )


def logout_doctor(request):

    request.session.pop('doctor_id', None)
    request.session.pop('doctor_name', None)

    return redirect('/')