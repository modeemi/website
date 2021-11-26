from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from modeemintternet.tasks import remind
from modeemintternet.models import Membership

@transaction.atomic
def spam(subject, message, memberships=None) -> List[str]:
    """
    Send message to all members.
    """

    # Default to members with fee paid this year or later
    if memberships is None:
        memberships = Membership.objects.exclude(Q(user__is_active=False))

    mailed = list(memberships.values_list("user__username", flat=True))

    if settings.MODE_DRY_RUN:
        logger.info("Would send to: %s", recipients)
        logger.info("Subject: %s", subject)
        logger.info("Body:")
        logger.info("%s", body)
        return recipients

    for membership in memberships:
        try:
            send_mail(subject, message, ORGANIZATION_EMAIL, [membership.user.email])
        except Exception as e:
            logger.exception(
                    "Sending email to %s failed",
                    membership.user,
                    exc_info=e,
                    )

    return reminded

class Command(BaseCommand):
    help = "Remind user accounts that have unpaid membership fees"

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
            contents.append(line)
        body = '\n'.join(lines)
        print("Press enter to confirm, ctrl-C to cancel.")
        input()
        spammed = spam()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully reminded {len(spammed)} accounts")
            )
