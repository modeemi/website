from datetime import datetime
from logging import getLogger

from django.conf import settings
from django.db import transaction

from modeemintternet.mailer import membership_remind, membership_deactivate

from modeemintternet.models import Membership, Passwd

logger = getLogger(__name__)


def remind():
    """
    Send reminder emails about unpaid membership fees.

    This function is to be run from a suitable task runner.
    """

    year = datetime.now().year
    memberships = Membership.objects.exclude(lifetime=True).exclude(user__is_active=False).exclude(
        fee__year__in=[
            year,
        ]
    )

    if settings.MODE_DRY_RUN:
        logger.info(f'Would remind: {list(memberships.values_list("user__username", flat=True))}')
        return

    for membership in memberships:
        try:
            membership_remind(membership)
            logger.warning('Sent membership fee reminder email to %s', membership.user)
        except Exception as e:
            logger.exception('Sending membership fee reminder email to %s failed', membership.user, exc_info=e)


def deactivate():
    """
    Deactivate accounts and send informative emails.

    This function is to be run from a suitable task runner.
    """

    year = datetime.now().year
    memberships = Membership.objects.exclude(lifetime=True).exclude(user__is_active=False).exclude(
        fee__year__in=[
            year - 1,
            year,
        ]
    )

    if settings.MODE_DRY_RUN:
        logger.info(f'Would deactivate: {list(memberships.values_list("user__username", flat=True))}')
        return

    with transaction.atomic('default'):
        with transaction.atomic(using='modeemiuserdb'):
            for membership in memberships:
                user = membership.user
                user.is_active = False
                user.save()

                if settings.MODE_TESTING:
                    continue

                passwd = Passwd.objects.get(username__iexact=user.username)
                passwd.shell = '/home/adm/bin/maksa'
                passwd.save()

    for membership in memberships:
        try:
            membership_deactivate(membership)
            logger.warning('Sent membership deactivation email to %s', membership.user)
        except Exception as e:
            logger.exception('Sending membership deactivation email to %s failed', membership.user, exc_info=e)
