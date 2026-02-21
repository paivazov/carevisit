from __future__ import annotations

from django.core.management.base import BaseCommand

from applications.utils.models import ControlSequence


class Command(BaseCommand):
    help = "Pre-fills ControlSequence with all defined sequence names"

    def handle(self, *args, **options) -> None:
        created_count = 0
        for value, label in ControlSequence.SequenceName.choices:
            _, created = ControlSequence.objects.get_or_create(name=value)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created sequence: {value}"))
            else:
                self.stdout.write(f"Already exists: {value}")

        self.stdout.write(self.style.SUCCESS(f"Done. {created_count} sequence(s) created."))
