from celery import shared_task
from django.utils import timezone

from applications.patient_visits.models import Visit


@shared_task
def mark_missed_visits():
    Visit.objects.filter(
        status=Visit.Status.SCHEDULED,
        end_date_time__lt=timezone.now(),
    ).update(status=Visit.Status.MISSED)
