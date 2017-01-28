# -*- coding: utf-8 -*-

"""
Custom mailer for the awesome modeemintternet super portal.
"""

from __future__ import unicode_literals

import textwrap

from django.conf import settings
from django.core.mail import send_mail


ORGANIZATION = 'Modeemi ry'
ORGANIZATION_EMAIL = settings.DEFAULT_FROM_EMAIL


def application_created(application):
    """
    Sends an email to the board notifying that
    a new membership application has been made.

    :param application: modeemintternet Application object.
    """

    # Creation notifier for the board
    subject = settings.EMAIL_SUBJECT_PREFIX + 'Uusi jäsenhakemus jätetty'
    body = \
"""
Hei,

henkilö {0} {1} ({2}) on jättänyt uuden jäsenhakemuksen {3}.

Voit tarkastella jäsenhakemusta osoitteessa:

    https://www.modeemi.fi/admin/modeemintternet/application/{4}/

Ystävällisin terveisin,
{5}n hallitusautomaatiobotti
""".format(application.first_name, application.last_name,
           application.primary_nick, application.applied.strftime('%d.%m.%Y'),
           application.id, ORGANIZATION)

    send_mail(subject, body, ORGANIZATION_EMAIL, [ORGANIZATION_EMAIL])

    # Notifier to the end user
    subject = settings.EMAIL_SUBJECT_PREFIX + 'Jäsenhakemuksesi lisätiedot'
    body = \
"""
Hei {0},

ja kiitos jäsenhakemuksestasi!

Käy maksamassa {7}n jäsenmaksu Holvin kaupassa, jos et ole vielä sitä ehtinyt tekemään:

    https://holvi.com/shop/modeemi/

Jos laskun maksaminen ei onnistu Holvissa niin:

- kysy ohjeet IRCissä: #modeemi @ IRCnet
- kysy ohjeet sähköpostilla hallitukselta: hallitus@modeemi.fi

Hallitus käsittelee hakemuksesi seuraavassa hallituksen kokouksessa.

Mikäli sinulla on kova kiire hakemuksen kanssa, voit olla hallitukseen yhteydessä sähköpostitse.

Ohessa hakemuksesi tiedot:

    Etunimi: {0}
    Sukunimi: {1}
    Sähköpostiosoite: {2}
    Ensisijainen tunnustoive: {3}
    Toissijainen tunnustoive: {4}
    Ensisijainen komentokehoite: {5}
    Hakemus jätetty: {6}

Ystävällisin terveisin,
{7}n hallitus
""".format(application.first_name, application.last_name,  application.email,
           application.primary_nick, application.secondary_nick, application.shell,
           application.applied.strftime('%d.%m.%Y'), ORGANIZATION)

    send_mail(subject, body, ORGANIZATION_EMAIL, [application.email])


def application_accepted(application):
    """
    Sends an email to an user notifying that his/her
    application has been processed and accepted.

    :param user: Django user object.
    """

    subject = settings.EMAIL_SUBJECT_PREFIX + 'Jäsenhakemuksesi on käsitelty'
    body = \
"""
Hei,

{0}n hallitus on käsitellyt ja hyväksynyt jäsenhakemuksesi.

Sinulle luodaan tunnus "{1}" tai "{2}" ja saat lisätiedot sähköpostissa.

Ystävällisin terveisin,
{0}n hallitus
""".format(ORGANIZATION,
           application.primary_nick,
           application.secondary_nick)

    send_mail(subject, body, ORGANIZATION_EMAIL, [application.email])

def application_rejected(application):
    """
    Sends an email to an user notifying that his/her
    application has been processed and rejected.

    :param application: modeemintternet Application object.
    """

    subject = settings.EMAIL_SUBJECT_PREFIX + 'Jäsenhakemuksesi on käsitelty'
    body = \
"""
Hei,

{0}n hallitus on käsitellyt ja ikävä kyllä hylännyt jäsenhakemuksesi.

Lisätietoja voit tulla tiedustelemaan kerhohuoneelta tai sähköpostitse osoitteesta {1}.

Ystävällisin terveisin,
{0}n hallitus
""".format(ORGANIZATION, ORGANIZATION_EMAIL)

    send_mail(subject, body, ORGANIZATION_EMAIL, [application.email])

def feedback_received(feedback):
    """
    Sends an email to the board notifying about new feedback.

    :param feedback: modeemintternet Feedback object.
    """

    subject = settings.EMAIL_SUBJECT_PREFIX + 'Palaute verkkosivujen kautta'
    body = \
"""
Hei,

Henkilö {0} on jättänyt seuraavan palautteen hallitukselle verkkosivujen välityksellä:

{1}

Voit tarkastella palautetta myös osoitteessa

    https://www.modeemi.fi/admin/modeemintternet/feedback/{2}/

Ystävällisin terveisin,
{3}n hallitusautomaatiobotti
""".format(
        feedback.sender,
        textwrap.fill(feedback.message),
        feedback.id,
        ORGANIZATION
    )

    send_mail(subject, body, ORGANIZATION_EMAIL, [ORGANIZATION_EMAIL])
