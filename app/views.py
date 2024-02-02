from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import PatientRegistrationForm, ClinicManagerRegistrationForm
from .models import Clinic, Appointment, User, Room


def register(request, register_type=None):
    form = None

    if request.method == 'POST':
        if register_type == 'manager':
            form = ClinicManagerRegistrationForm(request.POST)
        else:
            form = PatientRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            if register_type == 'manager':
                user.is_clinic_manager = True
                clinic = Clinic.objects.get(name=form.cleaned_data['clinic'])
                clinic.manager = user
            elif register_type == 'doctor':
                user.is_doctor = True
            else:
                user.is_patient = True

            user.save()
            return redirect('login')
    else:
        if register_type == 'manager':
            form = ClinicManagerRegistrationForm()
        else:
            form = PatientRegistrationForm()

    return render(request, 'register.html', {'form': form, 'register_type': register_type})


@login_required
def dashboard(request):
    user: User = request.user
    if user.is_clinic_manager:
        future_reservations = Appointment.objects.filter(room__clinic__manager=user, date_time__gt=timezone.now())
        past_reservations = Appointment.objects.filter(room__clinic__manager=user, date_time__lte=timezone.now())
    else:
        future_reservations = Appointment.objects.filter(patient=user, date_time__gt=timezone.now())
        past_reservations = Appointment.objects.filter(patient=user, date_time__lte=timezone.now())
    return render(request, 'app/dashboard.html',
                  {'future_reservations': future_reservations,
                   'past_reservations': past_reservations})


@login_required
def clinics_rooms(request):
    user: User = request.user
    if user.is_clinic_manager:
        clinics = Clinic.objects.filter(manager=user)
    else:
        clinics = Clinic.objects.filter(district=user.district)
    return render(request, 'app/clinics_rooms.html', {'clinics': clinics})

