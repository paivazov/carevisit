from django.conf import settings

from django.db import models

from applications.patient_visits.managers import VisitManager
from applications.utils.models import ControlSequence


class Duty(models.Model):
    name = models.CharField(max_length=255)
    duration = models.DurationField()

    class Meta:
        verbose_name_plural = 'duties'

    def __str__(self) -> str:
        return self.name


class Visit(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELED = 'canceled', 'Canceled'
        MISSED = 'missed', 'Missed'

    number = models.CharField(max_length=10, unique=True, editable=False)
    caregiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='caregiver_visits',
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='patient_visits',
    )
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
    duties = models.ManyToManyField(Duty, through='DutyResult', blank=True)
    description = models.TextField(max_length=500, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = VisitManager()

    def __str__(self) -> str:
        return f'Visit {self.number}'

    def save(self, *args, **kwargs) -> None:
        if not self.number:
            if not kwargs.get('number'):
                next_num = ControlSequence.get_next_number("visit_number")
                self.number = str(next_num).zfill(4)
        super().save(*args, **kwargs)


class DutyResult(models.Model):
    class Status(models.TextChoices):
        DONE = 'done', 'Done'
        NOT_DONE = 'not_done', 'Not Done'

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='duty_results')
    duty = models.ForeignKey(Duty, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.NOT_DONE,
    )

    class Meta:
        unique_together = ('visit', 'duty')

    def __str__(self) -> str:
        return f'{self.visit.number} - {self.duty.name}: {self.status}'
