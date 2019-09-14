from datetime import datetime
from logging import getLogger
from re import split

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from modeemintternet import mailer
from modeemintternet.models import News, Soda, Membership, MembershipFee
from modeemintternet.forms import ApplicationForm, FeedbackForm, MembershipForm, MembershipFeeForm
from modeemintternet.tasks import activate

logger = getLogger(__name__)


def sitemap(request):
    return render(request, 'sitemap.xml', content_type='application/xml')


def index(request):
    news = News.objects.order_by('-posted')[:10]
    return render(request, 'index.html', {'news': news})


def society(request):
    return render(request, 'society.html')


def saannot(request):
    return render(request, 'saannot.html')


def rekisteriseloste(request):
    return render(request, 'rekisteriseloste.html')


def hallitus(request):
    return render(request, 'hallitus.html')


def yhteystiedot(request):
    return render(request, 'yhteystiedot.html')


def backup(request):
    return render(request, 'backup.html')


def password(request):
    return render(request, 'password.html')


def halutaan(request):
    return render(request, 'halutaan.html')


def laitteisto(request):
    return render(request, 'laitteisto.html')


def palvelut(request):
    sodas = Soda.objects.filter(active=True).order_by('price', 'name')
    return render(request, 'palvelut.html', {'sodas': sodas})


def uutiset(request, pk=None):
    if pk:
        news = News.objects.filter(pk=pk)
    else:
        news = News.objects.order_by('-id')

    return render(request, 'uutiset.html', {'news': news})


def palaute(request):
    if not request.method == 'POST':
        return render(request, 'palaute.html', {'form': FeedbackForm()})

    feedback_form = FeedbackForm(request.POST)
    if not feedback_form.is_valid():
        return render(request, 'palaute.html', {
            'form': feedback_form,
        }, status=400)

    feedback = feedback_form.save()

    try:
        mailer.feedback_received(feedback)
    except Exception as e:
        logger.exception('Exception in sending feedback email', exc_info=e)

    return render(request, 'palaute.html', {
        'form': feedback_form,
        'feedback_saved': True,
    })


def jaseneksi(request):
    if not request.POST:
        return render(request, 'jaseneksi.html', {'form': ApplicationForm()})

    # Check form validity aside from passwords.
    application_form = ApplicationForm(request.POST)

    if not application_form.is_valid():
        return render(request, 'jaseneksi.html', {
            'form': application_form,
        }, status=400)

    # Password is not saved in the form, so we check it manually
    # and notify of errors in context the data, if there are any.
    password_matches = (
        request.POST.get('password') == request.POST.get('password_check')
    )

    # If the form is else valid but the password doesn't match or is empty,
    # mark the form as invalid and display a custom password error message.
    if not password_matches:
        error_msg = 'Salasana ja tarkiste eivät täsmää.'
        application_form.add_error('password', '')
        application_form.add_error('password_check', error_msg)

        return render(request, 'jaseneksi.html', {
            'form': application_form,
        }, status=400)

    application = application_form.save()
    application.generate_password_hashes(request.POST.get('password'))

    # Try and send mail about the application, otherwise log and show error message.
    try:
        mailing_success = True
        mailer.application_created(application)
    except Exception as e:
        mailing_success = False
        logger.error('Failed to send mail about the new application: %e', e)

    # Return info page for the application.
    return render(request, 'jaseneksi.html', {
        'application_saved': True,
        'mailing_success': mailing_success,
    })


@login_required
def kayttajatiedot(request):
    return render(request, 'tili/tiedot.html', {})


@login_required
@transaction.atomic
def kayttajatiedot_paivita(request):
    if request.method == 'POST':
        form = MembershipForm(request.POST)

        if form.is_valid():
            user = request.user
            membership, _ = Membership.objects.get_or_create(user=user)

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            membership.municipality = form.cleaned_data['municipality']

            user.save()
            membership.save()

            return HttpResponseRedirect(reverse('kayttajatiedot'))

    else:
        form = MembershipForm()

    return render(request, 'tili/paivita.html', {'form': form})


@login_required
@permission_required('modeemintternet.view_membership', raise_exception=True)
def kayttajarekisteri(request):
    memberships = Membership.objects.all().select_related('user').prefetch_related('fee')
    return render(request, 'rekisteri/rekisteri.html', {'memberships': memberships})


@login_required
@permission_required('modeemintternet.view_membership', raise_exception=True)
def kayttajarekisteri_listat(request):
    memberships = Membership.objects.all().select_related('user').prefetch_related('fee')
    emails = ', '.join((
        f'{first_name} {last_name} <{email}>'
        for first_name, last_name, email in
        memberships.values_list('user__first_name', 'user__last_name', 'user__email')
        if email
    ))

    return render(request, 'rekisteri/listat.html', {'memberships': memberships, 'emails': emails})


@login_required
@permission_required('modeemintternet.change_membership', raise_exception=True)
@transaction.atomic
def kayttajarekisteri_paivita(request, username: str):
    User = get_user_model()

    user = User.objects.get(username=username)
    membership, _ = Membership.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = MembershipForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            membership.municipality = form.cleaned_data['municipality']

            user.save()
            membership.save()

            return HttpResponseRedirect(reverse('kayttajarekisteri'))

    return render(request, 'rekisteri/paivita.html', {'membership': membership})


@login_required
@permission_required('modeemintternet.change_membership', raise_exception=True)
@transaction.atomic
def kayttajarekisteri_jasenmaksut(request):
    if request.method == 'POST':
        form = MembershipFeeForm(request.POST)

        if form.is_valid():
            year = form.cleaned_data['year']
            membership_fee, _ = MembershipFee.objects.get_or_create(year=year)

            usernames = list(filter(None, map(str.lower, map(str.strip,
                split(r'[\s,]+', form.cleaned_data['usernames']))
            )))

            memberships = Membership.objects.filter(user__username__in=usernames)
            membership_fee.membership_set.add(*memberships.values_list('pk', flat=True))

            # Activate users that have paid their membership fees.
            if year >= datetime.now().year:
                activate(memberships)

            return HttpResponseRedirect(reverse('kayttajarekisteri'))

    return render(request, 'rekisteri/jasenmaksut.html')
