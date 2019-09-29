from django.core.management.base import BaseCommand

from modeemintternet.tasks import deactivate


class Command(BaseCommand):
    help = "Deactivate user accounts that have unpaid membership fees"

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        deactivated = deactivate()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully deactivated {len(deactivated)} accounts")
        )
