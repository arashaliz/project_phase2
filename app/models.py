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

