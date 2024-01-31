from logging import getLogger

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q

from modeemintternet.models import Membership

logger = getLogger(__name__)

ORGANIZATION_EMAIL = settings.DEFAULT_FROM_EMAIL


@transaction.atomic
def spam(subject, message, memberships=None):
    """
    Send message to all members.
    """

    # Default to members with fee paid this year or later
    if memberships is None:
        memberships = Membership.objects.exclude(Q(user__is_active=False))

    if settings.MODE_DRY_RUN:
        reminded = list(memberships.values_list("user__username", flat=True))
        logger.info("Would send to: %s", reminded)
        logger.info("Subject: %s", subject)
        logger.info("Body:")
        logger.info(message)
        return reminded

    reminded = []
    for membership in memberships:
        try:
            send_mail(subject, message, ORGANIZATION_EMAIL, [membership.user.email])
            reminded.append(membership.user.username)
        except Exception as e:
            logger.exception("Sending email to %s failed", membership.user, exc_info=e)
    return reminded


class Command(BaseCommand):
    help = "Send email to all users"

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        print("Subject:")
        subject = input()
        print("Enter message body, ctrl-D to finish.")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            lines.append(line)
        message = "\n".join(lines)
        print("Press enter to confirm, ctrl-C to cancel.")
        input()
        spammed = spam(subject, message)
        self.stdout.write(
            self.style.SUCCESS(f"Successfully spammed {len(spammed)} accounts")
        )
