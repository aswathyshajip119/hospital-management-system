from django.shortcuts import render, redirect
from .models import Patient, Prescription, Report
from doctor.models import Doctor
from .models import Appointment
from datetime import date



from django.shortcuts import render

def home(request):
    return render(request, 'patient/home.html')


def register_patient(request):

    if request.method == "POST":
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']

        Patient.objects.create(
            name=name,
            age=age,
            gender=gender,
            phone=phone,
            email=email,
            address=address
        )

    return render(request, 'patient/register.html')


def patient_login(request):

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')

        try:
            patient = Patient.objects.get(email=email, name=name)

            request.session['patient_id'] = patient.id

            return redirect('/dashboard/')

        except Patient.DoesNotExist:
            return render(request, "patient/login.html", {
                "error": "Invalid credentials"
            })

    return render(request, "patient/login.html")


def book_appointment(request):

    patient_id = request.session.get('patient_id')

    if not patient_id:
        return redirect('/login/')

    patient = Patient.objects.get(id=patient_id)

    doctors = Doctor.objects.all()

    if request.method == "POST":

        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')

        doctor = Doctor.objects.get(id=doctor_id)

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date
        )

        return redirect('/dashboard/')

    return render(request, 'patient/book_appointment.html', {
        'doctors': doctors
    })



def patient_dashboard(request):

    patient_id = request.session.get('patient_id')

    if not patient_id:
        return redirect('/login/')

    patient = Patient.objects.get(id=patient_id)

    today = date.today()

    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        date__gte=today
    ).order_by('date')

    past_appointments = Appointment.objects.filter(
        patient=patient,
        date__lt=today
    ).order_by('-date')

    return render(request, "patient/dashboard.html", { "patient": patient,"upcoming_appointments": upcoming_appointments,
        "past_appointments": past_appointments
    })


def patient_prescriptions(request):

    patient_id = request.session.get('patient_id')

    if not patient_id:
        return redirect('/login/')

    patient = Patient.objects.get(id=patient_id)

    prescriptions = Prescription.objects.filter(
        patient=patient
    ).order_by('-date')

    return render(request, "patient/prescriptions.html", {
        "patient": patient,
        "prescriptions": prescriptions
    })


def patient_reports(request):

    patient_id = request.session.get('patient_id')

    if not patient_id:
        return redirect('/login/')

    patient = Patient.objects.get(id=patient_id)

    reports = Report.objects.filter(
        patient=patient
    ).order_by('-date')

    return render(request, "patient/reports.html", {
        "patient": patient,
        "reports": reports
    })


def cancel_appointment(request, appointment_id):

    patient_id = request.session.get('patient_id')

    if not patient_id:
        return redirect('/login/')

    try:
        appointment = Appointment.objects.get(
            id=appointment_id,
            patient_id=patient_id
        )

        appointment.status = "Cancelled"
        appointment.save()

    except Appointment.DoesNotExist:
        pass

    return redirect('/dashboard/')













def logout_patient(request):
    request.session.flush()
    return redirect('/')