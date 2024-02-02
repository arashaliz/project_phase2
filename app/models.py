from django.contrib.admin import site
from django.contrib.auth.models import AbstractUser
from django.db import models


class District(models.Model):
    location = models.CharField(max_length=255)


class User(AbstractUser):
    is_patient = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
    is_clinic_manager = models.BooleanField(default=False)
    district = models.ForeignKey(District, on_delete=models.deletion.SET_NULL, null=True, blank=True)

class Clinic(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class Room(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    doctor = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.doctor:
            return f"room_{self.id}_{self.clinic.name}_{self.doctor.username}"
        else:
            return f"room_{self.id}_{self.clinic.name}"


class Appointment(models.Model):
    reserved = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_time = models.DateTimeField()

