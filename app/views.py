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

