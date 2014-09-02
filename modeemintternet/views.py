# -*- coding: utf-8 -*-

import os
import settings

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.utils.timezone import now
from django.template import RequestContext

from reportlab.pdfgen import canvas

from .models import Application
from .forms import ApplicationForm

def render_with_context(request, template, params={}):
    return render_to_response(template, params,
                context_instance=RequestContext(request))

def etusivu(request):
    return render_with_context(request, 'etusivu.html')

def yhdistys(request):
    return render_with_context(request, 'yhdistys.html')

def palvelut(request):
    return render_with_context(request, 'palvelut.html')

def jaseneksi(request):
    return render_with_context(request, 'jaseneksi.html')

def laitteisto(request):
    return render_with_context(request, 'laitteisto.html')

def halutaan(request):
    return render_with_context(request, 'halutaan.html')

def hakemus(request):
    application_form = ApplicationForm()

    if not request.POST:
        return render_with_context(request, 'hakemus.html',
                {'form': application_form})

    else:
        application_form = ApplicationForm(request.POST)

        if not application_form.is_valid():
            return render_with_context(request, 'hakemus.html',
                {'form': application_form})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="modeemi-jasenhakemus.pdf"'

    application = application_form.save()

    # Create the PDF object, using the response object as its 'file.'
    p = canvas.Canvas(response)

    # Logo on top of the page
    # file, x, y
    logoPath = os.path.join(settings.PROJECT_DIR, 'static', 'modeemi-logo-bow.png')
    p.drawImage(logoPath, 50, 650, height=150, preserveAspectRatio=True, anchor='nw')

    # Text below the logo
    # x, y, text
    p.drawString(50, 600, 'Modeemi ry, jäsenhakemus')

    # Box containing the user information
    # x, y, width, height
    p.drawString(50, 560, 'Sähköposti')
    p.drawString(310, 560, application.email)
    p.rect(40, 550, 500, 30)
    p.drawString(50, 530, 'Nimi')
    p.drawString(310, 530, application.first_name + ' ' + application.last_name)
    p.rect(40, 520, 500, 30)
    p.drawString(50, 500, 'Peruste jäsenyyden hakemiselle')
    p.drawString(310, 500, application.reason)
    p.rect(40, 490, 500, 30)
    p.drawString(50, 470, 'Haluamani käyttäjätunnus')
    p.drawString(310, 470, application.primary_nick)
    p.rect(40, 460, 500, 30)
    p.drawString(50, 440, 'Jos jo käytössä')
    p.drawString(310, 440, application.secondary_nick)
    p.rect(40, 430, 500, 30)
    p.drawString(50, 410, 'Haluamani komentokehoite')
    p.drawString(310, 410, application.shell)
    p.rect(40, 400, 500, 30)

    # Line delimiting the pre-filled and user-filled parts
    # x1, y1, x2, y2
    p.line(300, 400, 300, 580)

    # Usage terms and signing line
    p.drawString(50, 360, 'Allekirjoitus: ')
    p.line(120, 358, 540, 358)
    p.drawString(50, 330, 'Modeemi ryn jäsenenä sitoudun FUNET:n käyttösääntöihin.')
    p.drawString(50, 300, 'Maksa jäsenmaksu, 8 euroa, tilille 224318-5739.')

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    return response
