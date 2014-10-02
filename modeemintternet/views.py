# -*- coding: utf-8 -*-

import os
import settings

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.utils.timezone import now
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required

from reportlab.pdfgen import canvas
from reportlab.graphics import renderSVG

from modeemintternet import helpers
from modeemintternet.models import Application, News
from modeemintternet.forms import ApplicationForm, NewsForm, NewsUpdateForm

def render_with_context(request, template, params={}):
    return render_to_response(template, params,
                context_instance=RequestContext(request))

def etusivu(request):
    news = News.objects.order_by('-posted')[:10]
    return render_with_context(request, 'etusivu.html', {'news': news})

def yhdistys(request):
    return render_with_context(request, 'yhdistys.html')

def palvelut(request):
    return render_with_context(request, 'palvelut.html')

def laitteisto(request):
    return render_with_context(request, 'laitteisto.html')

def jasenmaksu(request):
    return render_with_context(request, 'jasenmaksu.html')

def saannot(request):
    return render_with_context(request, 'saannot.html')

def hallitus(request):
    return render_with_context(request, 'hallitus.html')

def yhteystiedot(request):
    return render_with_context(request, 'yhteystiedot.html')

def backup(request):
    return render_with_context(request, 'backup.html')

def digipk(request):
    return render_with_context(request, 'digipk.html')

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

        if not application_form.is_valid():
            return render_with_context(request, 'jaseneksi.html',
                {'form': application_form})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="modeemi-jasenhakemus.pdf"'

    application = application_form.save()
    application.update_bank_reference()

    # Create the PDF object, using the response object as its 'file.'
    c = canvas.Canvas(response)
    p = helpers.jasenlasy(c, application)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    return response


def lue_uutisia(request, pk=None):
    if pk:
        return render_with_context(request, 'lue_uutisia.html',
                {'news': News.objects.filter(id=pk)})
    return render_with_context(request, 'lue_uutisia.html',
            {'news': News.objects.order_by('-id')[:20]})

@permission_required('news.can_create', login_url='/login/')
def luo_uutinen(request):
    news_form = NewsForm()

    if request.POST:
        news_form = NewsForm(request.POST)

        if news_form.is_valid():
            news = news_form.save()
            news.set_poster(request)

    return render_with_context(request, 'luo_uutinen.html',
            {'form': news_form})

@permission_required('news.can_modify', login_url='/login/')
def paivita_uutinen(request, pk):
    news_form = NewsUpdateForm(instance=News.objects.get(id=pk))

    if request.POST:
        news_form = NewsUpdateForm(request.POST, instance=News.objects.get(id=pk))

        if news_form.is_valid():
            news = news_form.save()
            news.set_modifier(request)

    return render_with_context(request, 'paivita_uutinen.html',
            {'form': news_form})
