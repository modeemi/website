from datetime import datetime
from logging import getLogger
from typing import List

from django.conf import settings
from django.db import transaction
from django.db.models import Q

from modeemintternet.mailer import membership_remind, membership_deactivate

from modeemintternet.models import Membership, Passwd

logger = getLogger(__name__)


def remind(memberships=None) -> List[str]:
    """
    Send reminder emails about unpaid membership fees.

    This function is to be run from a suitable task runner.
    """

    # Default to members with fee paid this year or later
    if memberships is None:
        memberships = Membership.objects.exclude(
            Q(lifetime=True)
            | Q(user__is_active=False)
            | Q(fee__year__gte=datetime.now().year)
        )

    reminded = list(memberships.values_list("user__username", flat=True))

    if settings.MODE_DRY_RUN:
        logger.info('Would remind: %s', reminded)
        return reminded

    for membership in memberships:
        try:
            membership_remind(membership)
            logger.warning('Sent membership fee reminder email to %s', membership.user)
        except Exception as e:
            logger.exception('Sending membership fee reminder email to %s failed', membership.user, exc_info=e)

    return reminded


def deactivate(memberships=None) -> List[str]:
    """
    Deactivate accounts and send informative emails.

    This function is to be run from a suitable task runner.
    """

    # Default to members with fee paid last year or later
    if memberships is None:
        memberships = Membership.objects.exclude(
            Q(lifetime=True)
            | Q(user__is_active=False)
            | Q(fee__year__gte=datetime.now().year - 1)
        )

    deactivated = list(memberships.values_list("user__username", flat=True))

    if settings.MODE_DRY_RUN:
        logger.info('Would deactivate: %s', deactivated)
        return deactivated

    with transaction.atomic('default'):
        with transaction.atomic(using='modeemiuserdb'):
            for membership in memberships:
                user = membership.user
                user.is_active = False
                user.save()

                # TODO: move all models to modeemiuserdb and make them managed so no flags are required
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

    return deactivated
