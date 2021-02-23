from datetime import datetime
from logging import getLogger
from re import split

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.timezone import now

from passlib.hash import md5_crypt, sha256_crypt, sha512_crypt

from modeemintternet import mailer
from modeemintternet.models import (
    Format,
    News,
    Soda,
    Membership,
    MembershipFee,
    Passwd,
    Shadow,
    ShadowFormat,
)
from modeemintternet.forms import (
    ApplicationForm,
    FeedbackForm,
    MembershipForm,
    MembershipFeeForm,
    PasswordForm,
)
from modeemintternet.tasks import activate


logger = getLogger(__name__)


def sitemap(request):
    return render(request, "sitemap.xml", content_type="application/xml")


def index(request):
    news = News.objects.order_by("-posted")[:10]
    return render(request, "index.html", {"news": news})


def society(request):
    return render(request, "society.html")


def rules(request):
    return render(request, "rules.html")


def policy(request):
    return render(request, "policy.html")


def board(request):
    return render(request, "board.html")


def contact(request):
    return render(request, "contact.html")


def backup(request):
    return render(request, "backup.html")


def password(request):
    return render(request, "password.html")


def wishlist(request):
    return render(request, "wishlist.html")


def hardware(request):
    return render(request, "hardware.html")


def services(request):
    sodas = Soda.objects.filter(active=True).order_by("price", "name")
    return render(request, "services.html", {"sodas": sodas})


def news(request, pk=None):
    if pk:
        news = News.objects.filter(pk=pk)
    else:
        news = News.objects.order_by("-id")

    return render(request, "news.html", {"news": news})


def feedback(request):
    if not request.method == "POST":
        return render(request, "feedback.html", {"form": FeedbackForm()})

    feedback_form = FeedbackForm(request.POST)
    if not feedback_form.is_valid():
        return render(request, "feedback.html", {"form": feedback_form}, status=400)

    feedback = feedback_form.save()

    try:
        mailer.feedback_received(feedback)
    except Exception as e:
        logger.exception("Exception in sending feedback email", exc_info=e)

    return render(
        request, "feedback.html", {"form": feedback_form, "feedback_saved": True}
    )


def application(request):
    if not request.POST:
        return render(request, "application.html", {"form": ApplicationForm()})

    # Check form validity aside from passwords.
    application_form = ApplicationForm(request.POST)

    if not application_form.is_valid():
        return render(
            request, "application.html", {"form": application_form}, status=400
        )

    # Password is not saved in the form, so we check it manually
    # and notify of errors in context the data, if there are any.
    password_matches = request.POST.get("password") == request.POST.get(
        "password_check"
    )

    # If the form is else valid but the password doesn't match or is empty,
    # mark the form as invalid and display a custom password error message.
    if not password_matches:
        error_msg = "Salasana ja tarkiste eivät täsmää."
        application_form.add_error("password", "")
        application_form.add_error("password_check", error_msg)

        return render(
            request, "application.html", {"form": application_form}, status=400
        )

    application = application_form.save()
    application.generate_password_hashes(request.POST.get("password"))

    # Try and send mail about the application, otherwise log and show error message.
    try:
        mailing_success = True
        mailer.application_created(application)
    except Exception as e:
        mailing_success = False
        logger.error("Failed to send mail about the new application: %e", e)

    # Return info page for the application.
    return render(
        request,
        "application.html",
        {"application_saved": True, "mailing_success": mailing_success},
    )


@login_required
def account_read(request):
    return render(request, "account/read.html", {})


@login_required
@transaction.atomic
def account_update(request):
    if request.method == "POST":
        form = MembershipForm(request.POST)

        if form.is_valid():
            user = request.user
            membership, _ = Membership.objects.get_or_create(user=user)

            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            membership.municipality = form.cleaned_data["municipality"]

            user.save()
            membership.save()

            return HttpResponseRedirect(reverse("account_read"))

    else:
        form = MembershipForm()

    return render(request, "account/update.html", {"form": form})


@login_required
@transaction.atomic
def password_update(request):
    if not request.POST:
        return render(request, "account/password.html", {"form": PasswordForm()})

    # Check form validity aside from passwords.
    form = PasswordForm(request.POST)
    if not form.is_valid():
        return render(request, "account/password.html", {"form": form}, status=400)

    # Check password validity for old password.
    username = request.user.username
    password = form.cleaned_data["password"]
    user = authenticate(request=request, username=username, password=password)
    if not user:
        error_msg = "Vanha salasana ei ole oikein."
        form.add_error("password", error_msg)

        return render(request, "account/password.html", {"form": form}, status=400)

    # Check password validity for new password and its check value.
    password_matches = (
        form.cleaned_data["new_password"] == form.cleaned_data["new_password_check"]
    )
    if not password_matches:
        error_msg = "Salasana ja tarkiste eivät täsmää."
        form.add_error("new_password", "")
        form.add_error("new_password_check", error_msg)

        return render(request, "account/password.html", {"form": form}, status=400)

    # If everything was OK update hash entries in the user database.
    last_updated = now()
    passwd = Passwd.objects.get(username=username)
    shadow = Shadow.objects.get(username=passwd)
    shadow.lastchanged = int(last_updated.timestamp()) // 86400
    shadow.save()

    # Delete all old hashes from the database
    # since this view is run inside a single atomic transaction
    # there is no risk of leaving the database to a defunct state
    ShadowFormat.objects.filter(username=passwd).delete()

    for f in Format.objects.all():
        # These are the currently updated hasher values
        # database formats table can have extra values but they are not processed
        h = {
            "SHA512": sha512_crypt.hash(password),
            "SHA256": sha256_crypt.hash(password),
            "MD5": md5_crypt.hash(password),
            "DES": "*LK*",  # ergo locked account https://en.wikipedia.org/wiki/Passwd
        }.get(f.format, None)

        # Write new hashes for supported formats
        if h:
            ShadowFormat.objects.create(
                username=passwd,
                format=f,
                hash=h,
                last_updated=last_updated,
            )

    return HttpResponseRedirect(reverse("account_read"))


@login_required
@permission_required("modeemintternet.view_membership", raise_exception=True)
def register_read(request):
    memberships = (
        Membership.objects.all().select_related("user").prefetch_related("fee")
    )
    return render(request, "register/read.html", {"memberships": memberships})


@login_required
@permission_required("modeemintternet.view_membership", raise_exception=True)
def register_emails(request):
    memberships = (
        Membership.objects.all().select_related("user").prefetch_related("fee")
    )
    emails = ", ".join(
        (
            f"{first_name} {last_name} <{email}>"
            for first_name, last_name, email in memberships.values_list(
                "user__first_name", "user__last_name", "user__email"
            )
            if email
        )
    )

    return render(
        request, "register/emails.html", {"memberships": memberships, "emails": emails}
    )


@login_required
@permission_required("modeemintternet.change_membership", raise_exception=True)
@transaction.atomic
def register_update(request, username: str):
    User = get_user_model()

    user = User.objects.get(username=username)
    membership, _ = Membership.objects.get_or_create(user=user)

    if request.method == "POST":
        form = MembershipForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            membership.municipality = form.cleaned_data["municipality"]

            user.save()
            membership.save()

            return HttpResponseRedirect(reverse("register_read"))

    return render(request, "register/update.html", {"membership": membership})


@login_required
@permission_required("modeemintternet.change_membership", raise_exception=True)
@transaction.atomic
def register_fees(request):
    if request.method == "POST":
        form = MembershipFeeForm(request.POST)

        if form.is_valid():
            year = form.cleaned_data["year"]
            membership_fee, _ = MembershipFee.objects.get_or_create(year=year)

            usernames = list(
                filter(
                    None,
                    map(
                        str.lower,
                        map(
                            str.strip, split(r"[\s,]+", form.cleaned_data["usernames"])
                        ),
                    ),
                )
            )

            memberships = Membership.objects.filter(user__username__in=usernames)
            membership_fee.membership_set.add(*memberships.values_list("pk", flat=True))

            # Activate users that have paid their membership fees.
            if year >= datetime.now().year:
                activate(memberships)

            return HttpResponseRedirect(reverse("register_read"))

    return render(request, "register/fees.html")
