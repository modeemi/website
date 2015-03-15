# -*- coding: utf-8 -*-

import os
import settings
from datetime import datetime, timedelta

# custom barcode module for Code 128 codes
import barcode
from barcode.writer import ImageWriter


def code128(application):
    """
    Creates a bank bar code in accordance to the Code 128 bank code spec

    Refer to:

        http://www.fkl.fi/en/material/publications/Publications/Bank_bar_code_guide.pdf

    I don't know why we needed this but it was cool to have.
    """

    version = str(4)
    iban = str(1022431800005739)
    eur = str(8).zfill(6)
    cents = str(0).zfill(2)
    reserve = str(0).zfill(3)
    reference = application.bank_reference.zfill(20)
    due_date = application.applied.strftime('%Y%m%d')

    joined = version + iban + eur + cents + reserve + reference + due_date

    return joined


def invoice(canvas, application):
    """
    Draw a membership invoice from to a canvas from an application objects.

    @param application {Application} modeemintternet.models.Application object
    @param canvas {Canvas} reportlab.pdfgen.canvas.Canvas object
    """

    p = canvas

    # Logo on top of the page
    textPath = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'static', 'logo', 'text.eps'))
    p.drawImage(textPath, 50, 710, height=100, preserveAspectRatio=True, anchor='nw')

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
    p.drawString(50, 500, 'Haluamani käyttäjätunnus')
    p.drawString(310, 500, application.primary_nick)
    p.rect(40, 490, 500, 30)
    p.drawString(50, 470, 'Jos jo käytössä')
    p.drawString(310, 470, application.secondary_nick)
    p.rect(40, 460, 500, 30)
    p.drawString(50, 440, 'Haluamani komentokehoite')
    p.drawString(310, 440, application.shell)
    p.rect(40, 430, 500, 30)
    p.drawString(50, 410, 'Hakemus tehty')
    p.drawString(310, 410, application.applied.strftime('%d.%m.%Y'))
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
    p.drawString(90, 175, application.first_name + ' ' + application.last_name)
    p.drawString(370, 80, application.bank_reference)
    deadline = application.applied + timedelta(days=21)
    p.drawString(370, 50, deadline.strftime('%d.%m.%Y'))
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

    generator = barcode.get_barcode_class('code128')
    img = generator(code128(application),
            writer=ImageWriter()).save('/tmp/barcode')
    p.drawImage(img, 150, 5, height=30, width=300, anchor='nw')

    return p
