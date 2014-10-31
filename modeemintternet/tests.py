# -*- coding: utf-8 -*-

"""
Unit tests for modeemintternet app.
"""

from django.test import Client, TestCase
from django.core import mail
from modeemintternet.forms import ApplicationForm


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
