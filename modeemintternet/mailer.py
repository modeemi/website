# -*- coding: utf-8 -*-

"""
Custom mailer for the awesome modeemintternet super portal.
"""

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from modeemintternet import helpers


ORGANIZATION = 'Modeemi ry'
ORGANIZATION_EMAIL = 'modeemi@modeemi.fi'


def application_created(application, invoice_pdf):
    """
    Sends an email to the board notifying that
    a new membership application has been made.

    :param application: modeemintternet Application object.
    """

    # Creation notifier for the board
    topic = u'{0} - Uusi jäsenhakemus jätetty'.format(ORGANIZATION)
    msg = \
u"""
Hei,

henkilö {0} {1} ({2}) on jättänyt uuden jäsenhakemuksen {3}.
Voit tarkastella jäsenhakemusta osoitteesta

    https://www.modeemi.fi/admin/modeemintternet/application/{4}/

Ystävällisin terveisin,
{5}n hallitusautomaatiobotti
""".format(application.first_name, application.last_name,
           application.primary_nick, application.applied.strftime('%d.%m.%Y'),
           application.id, ORGANIZATION)

    EmailMessage(topic, msg, ORGANIZATION, [ORGANIZATION_EMAIL]).send()

    # Notifier to the end user
    topic = u'{0} - Jäsenhakemuksesi lisätiedot'.format(ORGANIZATION)
    msg = \
u"""
Hei {0},

ja kiitos jäsenhakemuksestasi.

Ohessa on 8 euron suuruinen lasku jäsenmaksua varten.

Jäsenmaksun suorittamisen jälkeen hallitus käsittelee
hakemuksen seuraavassa hallituksen kokouksessa.
Mikäli sinulla on kova kiire hakemuksen kanssa,
voit olla hallitukseen yhteydessä sähköpostitse.

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

    invoice_name = 'modeemi_jasenhakemus_{0}.pdf'.format(application.id)
    invoice_mime = 'application/pdf'

    EmailMessage(topic, msg, ORGANIZATION, [application.email],
            attachments=[(invoice_name, invoice_pdf, invoice_mime)]).send()


def application_accepted(application):
    """
    Sends an email to an user notifying that his/her
    application has been processed and accepted.

    :param user: Django user object.
    """

    topic = u'{0} - Jäsenhakemuksesi on käsitelty'.format(ORGANIZATION)
    msg = \
u"""
Hei,

{0}n hallitus on käsitellyt ja hyväksynyt jäsenhakemuksesi.

Sinulle luodaan tunnus "{1}"/"{2}" ja saat lisätiedot sähköpostissa.

Ystävällisin terveisin,
{0}n hallitus
""".format(ORGANIZATION,
           application.primary_nick,
           application.secondary_nick)

    EmailMessage(topic, msg, ORGANIZATION, [application.email]).send()

def application_rejected(application):
    """
    Sends an email to an user notifying that his/her
    application has been processed and rejected.

    :param application: modeemintternet Application object.
    """

    topic = u'{0} - Jäsenhakemuksesi on käsitelty'.format(ORGANIZATION)
    msg = \
u"""
Hei,

{0}n hallitus on käsitellyt ja ikävä kyllä hylännyt jäsenhakemuksesi.

Tämä voi johtua riittämättömistä perusteluista tunnuksille
(et ole TTY:n opiskelijajäsen), tai sinulle ei ole voitu
myöntää jäsenyyttä ja tätä myöten tunnusta muusta syystä.

Lisätietoja voit tulla tiedustelemaan kerhohuoneelta tai
sähköpostitse osoitteesta {1}.

Ystävällisin terveisin,
{0}n hallitus
""".format(ORGANIZATION, ORGANIZATION_EMAIL)

    EmailMessage(topic, msg, ORGANIZATION, [application.email]).send()
