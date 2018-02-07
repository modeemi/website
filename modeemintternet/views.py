# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404


from modeemintternet import mailer
from modeemintternet.models import News, Event, Soda, Application
from modeemintternet.forms import ApplicationForm, FeedbackForm

logger = logging.getLogger(__name__)

def etusivu(request):
    news = News.objects.order_by('-posted')[:10]
    return render(request, 'etusivu.html', {'news': news})

def yhdistys(request):
    return render(request, 'yhdistys.html')

def palvelut(request):
    sodas = Soda.objects.filter(active=True).order_by('price', 'name')
    return render(request, 'palvelut.html', {'sodas': sodas})

def laitteisto(request):
    return render(request, 'laitteisto.html')

def palaute(request):
    feedback_form = FeedbackForm()

    if not request.POST:
        return render(request, 'palaute.html', {'form': feedback_form})

    else:
        feedback_form = FeedbackForm(request.POST)

        if not feedback_form.is_valid():
            return render(request, 'palaute.html',
                {'form': feedback_form}, status=400)

    feedback = feedback_form.save()
    mailer.feedback_received(feedback)

    return render(request, 'palaute.html',
            {'form': feedback_form, 'success': True})

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

def jaseneksi(request):
    application_form = ApplicationForm()

    if not request.POST:
        return render(request, 'jaseneksi.html', {'form': application_form})

    # Check form validity for password errors
    else:
        application_form = ApplicationForm(request.POST)

        # Password is not saved in the form, so we check it manually
        # and notify of errors in context the data, if there are any.
        password_matches = \
            request.POST.get('password') == request.POST.get('password_check')

        if not application_form.is_valid():
            return render(request, 'jaseneksi.html',
                    {'form': application_form}, status=400)

        # If the form is else valid but the password doesn't match or is empty,
        # mark the form as invalid and display a custom password error message.
        elif not password_matches:
            error_msg = 'Salasana ja tarkiste eivät täsmää.'
            application_form.add_error('password', '')
            application_form.add_error('password_check', error_msg)

            return render(request, 'jaseneksi.html',
                    {'form': application_form}, status=400)

    application = application_form.save()
    application.generate_password_hashes(request.POST.get('password'))

    # Try and send mail about the application, otherwise log and show error message.
    try:
        mailing_success = True
        mailer.application_created(application)
    except Exception as e:
        mailing_success = False
        logger.error('Failed to send mail about the new application: {}'.format(e))

    # Return info page for the application.
    return render(request, 'jaseneksi.html',
            {'success': True, 'mailing_success': mailing_success})

def uutiset(request, pk=None):
    if pk:
        return render(request, 'uutiset.html',
                {'news': News.objects.filter(pk=pk)})
    return render(request, 'uutiset.html',
            {'news': News.objects.order_by('-id')})


def sitemap(request):
    return render(request, 'sitemap.xml', content_type='application/xml')
