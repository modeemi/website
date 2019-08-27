from datetime import datetime
from logging import getLogger
from typing import List

from django.conf import settings
from django.db import transaction
from django.db.models import Q

from modeemintternet.mailer import membership_remind, membership_deactivate, membership_activate

from modeemintternet.models import Membership, Passwd

logger = getLogger(__name__)


@transaction.atomic
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


@transaction.atomic
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

    deactivated = list()
    for membership in memberships:
        active = False

        user = membership.user
        if user.is_active:
            active = True
            user.is_active = False
            user.save()

        try:
            passwd = Passwd.objects.get(username__iexact=user.username)
            if passwd.shell != settings.MODEEMI_SHELL_INACTIVE:
                active = True
                passwd.shell = settings.MODEEMI_SHELL_INACTIVE
                passwd.save()
        except Passwd.DoesNotExist:
            pass

        if not active:
            continue

        deactivated.append(user.username)
        try:
            membership_deactivate(membership)
            logger.warning('Sent membership deactivation email to %s', membership.user)
        except Exception as e:
            logger.exception('Sending membership deactivation email to %s failed', membership.user, exc_info=e)

    return deactivated


@transaction.atomic
def activate(memberships=None) -> List[str]:
    if memberships is None:
        memberships = Membership.objects.filter(user__is_active=False, fee__year__gte=datetime.now().year)

    activated = list()
    for membership in memberships:
        inactive = False

        user = membership.user
        if not user.is_active:
            inactive = True
            user.is_active = True
            user.save()

        try:
            passwd = Passwd.objects.get(username__iexact=user.username)
            if passwd.shell == settings.MODEEMI_SHELL_INACTIVE:
                inactive = True
                passwd.shell = '/bin/bash'
            passwd.save()
        except Passwd.DoesNotExist:
            pass

        if not inactive:
            continue

        activated.append(user.username)
        try:
            membership_activate(membership)
            logger.warning('Sent membership activation email to %s', membership.user)
        except Exception as e:
            logger.exception('Sending membership activation email to %s failed', membership.user, exc_info=e)

    return activated
