# -*- coding: utf-8 -*-

import os
import settings

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.utils.timezone import now
from django.template import RequestContext

from reportlab.pdfgen import canvas
from reportlab.graphics import renderSVG

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
    p = canvas.Canvas(response)

    # Logo on top of the page
    textPath = os.path.join(settings.PROJECT_DIR, 'static', 'logo', 'text.eps')
    wizardPath = os.path.join(settings.PROJECT_DIR, 'static', 'logo', 'wizard.eps')
    p.drawImage(textPath, 50, 710, height=100, preserveAspectRatio=True, anchor='nw')
    p.drawImage(wizardPath, 310, 500, height=350, preserveAspectRatio=True, anchor='nw')

    p.drawString(70, 720, 'Modeemi ry c/o TTY')
    p.drawString(70, 700, 'PL 553')
    p.drawString(70, 680, 'FIN-33101 Tampere')

    # Box containing the user information
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
    p.line(300, 400, 300, 580)

    # Draw the bank information grid
    # Horizontal lines
    p.line(0, 40, 600, 40)
    p.line(0, 70, 600, 70)
    p.line(300, 100, 600, 100)
    p.line(0, 200, 300, 200)
    p.line(0, 250, 600, 250)
    p.line(0, 300, 600, 300)

    # Vertical lines
    p.line(300, 40, 300, 300)
    p.line(350, 40, 350, 100)
    p.line(450, 40, 450, 70)
    p.line(70, 200, 70, 300)

    # Texts
    p.drawString(90, 270, 'FI10 2243 1800 0057 39')
    p.drawString(320, 270, 'NDEAFIHH')
    p.drawString(90, 220, 'Modeemi ry')
    p.drawString(370, 80, application.bank_reference[0:3] +
            ' ' + application.bank_reference[3:-1])
    p.drawString(550, 50, '8,00')

    p.setFontSize(7)
    p.drawString(40, 290, 'Tilinro')
    p.drawString(80, 290, 'IBAN')
    p.drawString(310, 290, 'BIC')
    p.drawString(40, 240, 'Saaja')
    p.drawString(310, 90, 'Viitenro')
    p.drawString(310, 60, 'Eräpäivä')
    p.drawString(460, 60, 'Euro')

    p.drawString(30, 180, 'Maksajan')
    p.drawString(39, 170, 'nimi ja')
    p.drawString(41, 160, 'osoite')

    p.drawString(45, 95, 'Alle-')
    p.drawString(33, 85, 'kirjoitus')

    p.line(70, 80, 300, 80)

    p.drawString(30, 60, 'Tililtä nro')

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    return response
