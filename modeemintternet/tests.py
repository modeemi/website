# -*- coding: utf-8 -*-

"""
Unit tests for modeemintternet app.
"""

from django.test import Client, TestCase
from django.core import mail

from modeemintternet.models import Application
from modeemintternet.forms import ApplicationForm
from modeemintternet.mailer import application_accepted, application_rejected


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
            'reason': 'Koska voi',
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

