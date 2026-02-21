from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class ProfileType(models.TextChoices):
        CAREGIVER = 'caregiver', 'Caregiver'
        PATIENT = 'patient', 'Patient'

    profile_type = models.CharField(
        max_length=20,
        choices=ProfileType.choices,
        blank=True,
    )
