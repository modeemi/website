"""
Custom mailer for the awesome modeemintternet super portal.
"""

from textwrap import fill

from django.conf import settings
from django.core.mail import send_mail


ORGANIZATION = "Modeemi ry"
ORGANIZATION_EMAIL = settings.DEFAULT_FROM_EMAIL
ORGANIZATION_WEBSHOP = "https://holvi.com/shop/modeemi/"


def application_created(application):
    """
    Sends an email to the board notifying that
    a new membership application has been made.

    :param application: modeemintternet Application object.
    """

    # Creation notifier for the board
    subject = settings.EMAIL_SUBJECT_PREFIX + "Uusi jäsenhakemus jätetty"
    body = f"""
Hei,

henkilö {application.first_name} {application.last_name} ({application.username})
on jättänyt uuden jäsenhakemuksen {application.applied.strftime}.

Voit tarkastella jäsenhakemusta osoitteessa:

    https://www.modeemi.fi/admin/modeemintternet/application/{application.id}/

Ystävällisin terveisin,
{ORGANIZATION}n hallitusautomaatiobotti
"""

    send_mail(subject, body, ORGANIZATION_EMAIL, [ORGANIZATION_EMAIL])

    # Notifier to the end user
    key_needed = "Kyllä" if application.virtual_key_required else "Ei"
    application_time = application.applied.strftime("%d.%m.%Y")
    subject = settings.EMAIL_SUBJECT_PREFIX + "Jäsenhakemuksesi lisätiedot"
    body = f"""
Hei {application.first_name},

ja kiitos jäsenhakemuksestasi!

Käy maksamassa {ORGANIZATION}n jäsenmaksu Holvin kaupassa, jos et ole vielä sitä ehtinyt tekemään:

    {ORGANIZATION_WEBSHOP}

Jos laskun maksaminen ei onnistu Holvissa niin:

- kysy ohjeet IRCissä: #modeemi @ IRCnet
- kysy ohjeet sähköpostilla hallitukselta: hallitus@modeemi.fi

Hallitus käsittelee hakemuksesi seuraavassa hallituksen kokouksessa.

Mikäli sinulla on kova kiire hakemuksen kanssa, voit olla hallitukseen yhteydessä sähköpostitse.

Ohessa hakemuksesi tiedot:

    Etunimi: {application.first_name}
    Sukunimi: {application.last_name}
    Sähköpostiosoite: {application.email}
    Tunnus: {application.username}
    Komentokehoite: {application.shell}
    Virtuaaliavain: {key_needed}
    Hakemus jätetty: {application_time}

Ystävällisin terveisin,
{ORGANIZATION}n hallitus
"""

    send_mail(subject, body, ORGANIZATION_EMAIL, [application.email])


def application_accepted(application):
    """
    Sends an email to an user notifying that his/her
    application has been processed and accepted.

    :param user: Django user object.
    """

    subject = settings.EMAIL_SUBJECT_PREFIX + "Jäsenhakemuksesi on käsitelty"
    body = f"""
Hei,

{ORGANIZATION}n hallitus on käsitellyt ja hyväksynyt jäsenhakemuksesi.

Sinulle on luotu tunnus {application.username}.

Tunnuksien jakelu jäsenkoneille tehdään öisin, joten kirjautuminen onnistuu vasta seuraavana päivänä.

Ystävällisin terveisin,
{ORGANIZATION}n hallitus
"""

    send_mail(subject, body, ORGANIZATION_EMAIL, [application.email])


def application_rejected(application):
    """
    Sends an email to an user notifying that his/her
    application has been processed and rejected.

    :param application: modeemintternet Application object.
    """

    subject = settings.EMAIL_SUBJECT_PREFIX + "Jäsenhakemuksesi on käsitelty"
    body = """
Hei,

{ORGANIZATION}n hallitus on käsitellyt ja ikävä kyllä hylännyt jäsenhakemuksesi.

Lisätietoja voit tulla tiedustelemaan kerhohuoneelta tai sähköpostitse osoitteesta {ORGANIZATION_EMAIL}.

Ystävällisin terveisin,
{ORGANIZATION}n hallitus
"""

    send_mail(subject, body, ORGANIZATION_EMAIL, [application.email])


def feedback_received(feedback):
    """
    Sends an email to the board notifying about new feedback.

    :param feedback: modeemintternet Feedback object.
    """

    subject = settings.EMAIL_SUBJECT_PREFIX + "Palaute verkkosivujen kautta"
    body = f"""
Hei,

henkilö {feedback.sender} on jättänyt seuraavan palautteen hallitukselle verkkosivujen välityksellä:

{fill(feedback.message)}

Voit tarkastella palautetta myös osoitteessa

    https://www.modeemi.fi/admin/modeemintternet/feedback/{feedback.id}/

Ystävällisin terveisin,
{ORGANIZATION}n hallitusautomaatiobotti
"""

    send_mail(subject, body, ORGANIZATION_EMAIL, [ORGANIZATION_EMAIL])


def membership_remind(membership):
    """
    Sends an email to a member notifying about a missing payment.

    :param membership: modeemintternet Membership object.
    """

    subject = settings.EMAIL_SUBJECT_PREFIX + "Tunnus sulkeutumassa"
    body = f"""
Hei {membership.user.username},

automaattinen järjestelmämme on huomannut, että et ole vielä suorittanut kuluvan vuoden jäsenmaksua.

Voit maksaa jäsenmaksun helposti itsepalveluna osoitteessa

    https://holvi.com/shop/modeemi/

Mikäli et maksa jäsenmaksua, tunnuksesi kerhon järjestelmiin sulkeutuu automaattisesti.

Mikäli olet suorittanut maksun jotakin muuta kautta, mutta se ei ole
jostakin syystä kirjautunut jäsenmaksujen seurantajärjestelmäämme,
voit olla yhteydessä kerhon hallitukseen sähköpostilla tai IRCissä.

Ystävällisin terveisin,
{ORGANIZATION}n hallitusautomaatiobotti
"""

    send_mail(subject, body, ORGANIZATION_EMAIL, [membership.user.email])


def membership_deactivate(membership):
    """
    Sends an email to a member notifying about membership deactivation.

    :param membership: modeemintternet Membership object.
    """

    subject = settings.EMAIL_SUBJECT_PREFIX + "Tunnus suljettu"
    body = f"""
Hei {membership.user.username},

tunnuksesi on suljettu maksamattoman jäsenmaksun tai muun syyn vuoksi.

Ystävällisin terveisin,
{ORGANIZATION}n hallitusautomaatiobotti
"""

    send_mail(subject, body, ORGANIZATION_EMAIL, [membership.user.email])


def membership_activate(membership):
    """
    Sends an email to a member notifying about membership activation.

    :param membership: modeemintternet Membership object.
    """

    subject = settings.EMAIL_SUBJECT_PREFIX + "Tunnus avattu"
    body = f"""
Hei {membership.user.username},

tunnuksesi Modeemin järjestelmiin on avattu.

Ystävällisin terveisin,
{ORGANIZATION}n hallitusautomaatiobotti
"""

    send_mail(subject, body, ORGANIZATION_EMAIL, [membership.user.email])
