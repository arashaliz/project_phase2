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


@login_required
def room_times(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    user: User = request.user

    if user.is_patient:
        appointments = Appointment.objects.filter(room=room, reserved=False)
        return render(request, 'app/room_times.html', {'room': room, 'appointments': appointments})
    elif user.is_clinic_manager or user.is_doctor:
        appointments = Appointment.objects.filter(room=room)
        return render(request, 'app/room_times.html', {'room': room, 'appointments': appointments})


@login_required
def update_capacity(request, room_id):
    if request.method == 'POST' and request.user.is_clinic_manager:
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M')

        try:
            room = Room.objects.get(id=room_id)
            room.save()

            time_increment = timedelta(minutes=30)
            num_appointments = int((end_time - start_time).total_seconds() / 1800)
            for _ in range(num_appointments):
                Appointment.objects.create(room=room, date_time=start_time)
                start_time += time_increment

            return JsonResponse({'success': True, 'message': 'Capacity updated successfully'})
        except Room.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Room not found'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'}, status=500)

    return HttpResponseBadRequest('Invalid request')


@login_required
def reserve_time(request, room_id):
    if request.method == 'POST' and request.user.is_patient:
        try:
            date_time = request.POST.get('date_time')
            appointment = Appointment.objects.get(date_time=date_time, room_id=room_id, reserved=False)
            appointment.reserved = True
            appointment.patient = request.user
            appointment.save()

            return JsonResponse({'success': True, 'message': 'Reservation successful'})
        except Appointment.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Appointment not found or already reserved'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'}, status=500)

    return HttpResponseBadRequest('Invalid request')
