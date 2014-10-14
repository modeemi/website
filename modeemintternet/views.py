# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from reportlab.pdfgen import canvas

from modeemintternet import mailer, helpers
from modeemintternet.models import Soda, News
from modeemintternet.forms import ApplicationForm, FeedbackForm

def render_with_context(request, template, params={}):
    return render_to_response(template, params,
                context_instance=RequestContext(request))

def etusivu(request):
    news = News.objects.order_by('-posted')[:10]
    return render_with_context(request, 'etusivu.html', {'news': news})

def yhdistys(request):
    return render_with_context(request, 'yhdistys.html')

def palvelut(request):
    sodas = Soda.objects.filter(active=True).order_by('price', 'name')
    return render_with_context(request, 'palvelut.html', {'sodas': sodas})

def laitteisto(request):
    return render_with_context(request, 'laitteisto.html')

def palaute(request):
    feedback_form = FeedbackForm()

    if not request.POST:
        return render_with_context(request, 'palaute.html',
                {'form': feedback_form})

    else:
        feedback_form = FeedbackForm(request.POST)

        if not feedback_form.is_valid():
            return render_with_context(request, 'palaute.html',
                {'form': feedback_form})

    feedback = feedback_form.save()
    return render_with_context(request, 'palaute.html',
            {'form': feedback_form, 'success': True})

def saannot(request):
    return render_with_context(request, 'saannot.html')

def hallitus(request):
    return render_with_context(request, 'hallitus.html')

def yhteystiedot(request):
    return render_with_context(request, 'yhteystiedot.html')

def backup(request):
    return render_with_context(request, 'backup.html')

def password(request):
    return render_with_context(request, 'password.html')

def halutaan(request):
    return render_with_context(request, 'halutaan.html')

def jaseneksi(request):
    application_form = ApplicationForm()

    if not request.POST:
        return render_with_context(request, 'jaseneksi.html',
                {'form': application_form})

    else:
        application_form = ApplicationForm(request.POST)
        password_matches = \
            request.POST.get('password') == request.POST.get('password_check')

        if not (password_matches and application_form.is_valid()):
            return render_with_context(request, 'jaseneksi.html',
                                       {'form': application_form})


    application = application_form.save()
    application.generate_password_hashes(request.POST.get('password'))
    application.update_bank_reference()

    # Create the PDF object, using the response object as the file-like object.
    c = canvas.Canvas()
    p = helpers.jasenlasy(c, application)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # Send mail about the new application
    mailer.application_created(application, p)

    # Return info page for the application
    return render_with_context(request, 'jaseneksi.html', {'success': True})

def uutiset(request, pk=None):
    if pk:
        return render_with_context(request, 'uutiset.html',
                {'news': News.objects.filter(id=pk)})
    return render_with_context(request, 'uutiset.html',
            {'news': News.objects.order_by('-id')[:20]})
