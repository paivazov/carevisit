from django.db import models
from applications.utils.models import ControlSequence


class VisitManager(models.Manager):
    def without_deleted(self):
        return super().get_queryset().filter(is_deleted=False)

    def bulk_create(self, objs, **kwargs):
        without_number = [obj for obj in objs if not obj.number]
        if without_number:
            numbers = ControlSequence.get_next_number_range(ControlSequence.SequenceName.VISIT_NUMBER, len(without_number))
            for obj, num in zip(without_number, numbers):
                obj.number = str(num).zfill(4)
        return super().bulk_create(objs, **kwargs)