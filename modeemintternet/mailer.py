"""
Custom mailer for the awesome modeemintternet super portal.
"""

from textwrap import fill

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
    body = f"""
Hei,

henkilö {0} {1} ({2}) on jättänyt uuden jäsenhakemuksen {3}.

Voit tarkastella jäsenhakemusta osoitteessa:

    https://www.modeemi.fi/admin/modeemintternet/application/{4}/

Ystävällisin terveisin,
{5}n hallitusautomaatiobotti
""".format(
        application.first_name,
        application.last_name,
        application.username,
        application.applied.strftime('%d.%m.%Y'),
        application.id,
        ORGANIZATION,
    )

    send_mail(subject, body, ORGANIZATION_EMAIL, [ORGANIZATION_EMAIL])

    # Notifier to the end user
    subject = settings.EMAIL_SUBJECT_PREFIX + 'Jäsenhakemuksesi lisätiedot'
    body = """
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
    Tunnus: {3}
    Komentokehoite: {4}
    Virtuaaliavain: {5}
    Hakemus jätetty: {6}

Ystävällisin terveisin,
{7}n hallitus
""".format(
        application.first_name,
        application.last_name,
        application.email,
        application.username,
        application.shell,
        'Kyllä' if application.virtual_key_required else 'Ei',
        application.applied.strftime('%d.%m.%Y'),
        ORGANIZATION,
    )

    send_mail(subject, body, ORGANIZATION_EMAIL, [application.email])


def application_accepted(application):
    """
    Sends an email to an user notifying that his/her
    application has been processed and accepted.

    :param user: Django user object.
    """

    subject = settings.EMAIL_SUBJECT_PREFIX + 'Jäsenhakemuksesi on käsitelty'
    body = """
Hei,

{0}n hallitus on käsitellyt ja hyväksynyt jäsenhakemuksesi.

Sinulle on luotu tunnus {1}.

Tunnuksien jakelu jäsenkoneille tehdään öisin, joten kirjautuminen onnistuu vasta seuraavana päivänä.

Ystävällisin terveisin,
{0}n hallitus
""".format(
        ORGANIZATION,
        application.username,
    )

    send_mail(subject, body, ORGANIZATION_EMAIL, [application.email])


def application_rejected(application):
    """
    Sends an email to an user notifying that his/her
    application has been processed and rejected.

    :param application: modeemintternet Application object.
    """

    subject = settings.EMAIL_SUBJECT_PREFIX + 'Jäsenhakemuksesi on käsitelty'
    body = """
Hei,

{0}n hallitus on käsitellyt ja ikävä kyllä hylännyt jäsenhakemuksesi.

Lisätietoja voit tulla tiedustelemaan kerhohuoneelta tai sähköpostitse osoitteesta {1}.

Ystävällisin terveisin,
{0}n hallitus
""".format(
        ORGANIZATION,
        ORGANIZATION_EMAIL
    )

    send_mail(subject, body, ORGANIZATION_EMAIL, [application.email])


def feedback_received(feedback):
    """
    Sends an email to the board notifying about new feedback.

    :param feedback: modeemintternet Feedback object.
    """

    subject = settings.EMAIL_SUBJECT_PREFIX + 'Palaute verkkosivujen kautta'
    body = """
Hei,

henkilö {0} on jättänyt seuraavan palautteen hallitukselle verkkosivujen välityksellä:

{1}

Voit tarkastella palautetta myös osoitteessa

    https://www.modeemi.fi/admin/modeemintternet/feedback/{2}/

Ystävällisin terveisin,
{3}n hallitusautomaatiobotti
""".format(
        feedback.sender,
        fill(feedback.message),
        feedback.id,
        ORGANIZATION,
    )

    send_mail(subject, body, ORGANIZATION_EMAIL, [ORGANIZATION_EMAIL])


def membership_remind(membership):
    """
    Sends an email to a member notifying about a missing payment.

    :param membership: modeemintternet Membership object.
    """

    subject = settings.EMAIL_SUBJECT_PREFIX + 'Tunnus sulkeutumassa'
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

    subject = settings.EMAIL_SUBJECT_PREFIX + 'Tunnus suljettu'
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

    subject = settings.EMAIL_SUBJECT_PREFIX + 'Tunnus avattu'
    body = f"""
Hei {membership.user.username},

tunnuksesi Modeemin järjestelmiin on avattu.

Ystävällisin terveisin,
{ORGANIZATION}n hallitusautomaatiobotti
"""

    send_mail(subject, body, ORGANIZATION_EMAIL, [membership.user.email])
