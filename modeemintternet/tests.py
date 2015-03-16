# -*- coding: utf-8 -*-

"""
Unit tests for modeemintternet app.
"""

from django.test import Client, TestCase
from django.core import mail
from django.core.urlresolvers import reverse

from modeemintternet.models import Application
from modeemintternet.forms import ApplicationForm
from modeemintternet.mailer import application_accepted, application_rejected

class FeedTest(TestCase):
    def test_news_rss_feed_response_codes(self):
        c = Client()
        response = c.get('/feed/uutiset.rss')
        self.assertEqual(response.status_code, 200)

    def test_event_rss_feed_response_codes(self):
        c = Client()
        response = c.get('/feed/tapahtumat.rss')
        self.assertEqual(response.status_code, 200)

    def test_event_ical_feed_response_codes(self):
        c = Client()
        response = c.get('/feed/tapahtumat.ics')
        self.assertEqual(response.status_code, 200)

class MembershipApplicationTest(TestCase):
    """
    Test making a new application via the form.
    """

    pass


class FeedbackTest(TestCase):
    """
    Test leaving feedback via the form.
    """

    pass


class ApplicationMailerTest(TestCase):
    """
    Check that mail is sent to users when creating an application.
    Note that you still need valid mail server in addition to this.
    """

    def setUp(self):
        self.application = {
            'email': 'teemu@teekkari.fi',
            'first_name': 'Teemu',
            'last_name': 'Testaaja',
            'primary_nick': 'teemut',
            'secondary_nick': 'testaajat',
            'shell': '/bin/zsh',
            'funet_rules_accepted': True,
            'password': 'testi',
            'password_check':'testi'
        }

    def test_application_made(self):
        """
        Test that mail is sent when an application is made.
        """

        c = Client()
        response = c.post('/jaseneksi/', self.application)

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, u'Modeemi ry - Uusi jäsenhakemus jätetty')
        self.assertEqual(mail.outbox[1].subject, u'Modeemi ry - Jäsenhakemuksesi lisätiedot')

    def test_application_accepted(self):
        del self.application['password']
        del self.application['password_check']

        a = Application(**self.application)
        a.save()
        a.generate_password_hashes('testi')
        a.update_bank_reference()
        a.save()

        application_accepted(a)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, u'Modeemi ry - Jäsenhakemuksesi on käsitelty')

    def test_application_rejected(self):
        del self.application['password']
        del self.application['password_check']

        a = Application(**self.application)
        a.save()
        a.generate_password_hashes('testi')
        a.update_bank_reference()
        a.save()

        application_rejected(a)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, u'Modeemi ry - Jäsenhakemuksesi on käsitelty')


class ApplicationBankReferenceNumberTest(TestCase):
    """
    Test the generation of an user bank reference number.
    """

    def setUp(self):
        self.application = Application(
                first_name='Pekka',
                last_name='Sauron',
                email='pekka.sauron@mordor.com',
                primary_nick='pekkas',
                secondary_nick='sauronp',
                shell=Application.BASH,
                funet_rules_accepted=True)

        self.application.save()
        self.application.generate_password_hashes(password='pekkaonparas:D')
        self.application.update_bank_reference()

    def test_reference_number_genration(self):
        """
        Test that an application's reference number is calculated correctly.

        Preceding zeros don't actually matter,
        we're just padding the numbers for consistency.
        """

        comparisons = [
                (1, '00013'),
                (2, '00026'),
                (3, '00039'),
                (42, '00424'),
                (420, '04200'),
                (666, '06664'),
                (9001, '90010')
        ]

        for (id, bank_reference) in comparisons:
            self.application.id = id
            self.application.save()
            self.application.update_bank_reference()
            self.application.save()

            self.assertEqual(self.application.bank_reference, bank_reference)
