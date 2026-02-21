from django.db import models, transaction

class ControlSequence(models.Model):
    class SequenceName(models.TextChoices):
        VISIT_NUMBER = 'visit_number', 'Visit model number seq'

    name = models.CharField(max_length=100, unique=True, choices=SequenceName.choices)
    sequence_number = models.IntegerField(default=0)

    @classmethod
    def get_next_number(cls, sequence_name):
        return cls.get_next_number_range(sequence_name, 1)[0]

    @classmethod
    @transaction.atomic
    def get_next_number_range(cls, sequence_name: str, count: int) -> range:
        sequence = cls.objects.select_for_update().get(name=sequence_name)
        start = sequence.sequence_number + 1
        sequence.sequence_number = models.F("sequence_number") + count
        sequence.save()
        return range(start, start + count)
