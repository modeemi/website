from django.core.management.base import BaseCommand

from modeemintternet.tasks import remind


class Command(BaseCommand):
    help = 'Remind user accounts that have unpaid membership fees'

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        reminded = remind()
        self.stdout.write(self.style.SUCCESS(f'Successfully reminded {len(reminded)} accounts'))
