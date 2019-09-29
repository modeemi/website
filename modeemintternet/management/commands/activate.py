from django.core.management.base import BaseCommand

from modeemintternet.tasks import activate


class Command(BaseCommand):
    help = "Activate user accounts that have paid membership fees"

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        activated = activate()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully activated {len(activated)} accounts")
        )
