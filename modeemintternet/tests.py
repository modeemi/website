# -*- coding: utf-8 -*-

"""
Unit tests for modeemintternet app.
"""

from __future__ import unicode_literals

import datetime
import sys
import unittest

from django.test import Client, TestCase
from django.core import mail
from django.utils import timezone

from modeemintternet.models import Application, Feedback, News, Event, Soda
from modeemintternet.mailer import application_accepted, application_rejected


class ViewGetTest(TestCase):
    def setUp(self):
        self.urls = [
            '/'
            , '/ry/'
            , '/palvelut/'
            , '/jaseneksi/'
            , '/laitteisto/'
            , '/palaute/'
            , '/uutineet/'
            , '/tapahtumat/'
            , '/ry/saannot/'
            , '/ry/rekisteriseloste/'
            , '/ry/hallitus/'
            , '/ry/yhteystiedot/'
            , '/palvelut/backup/'
            , '/palvelut/password/'
            , '/laitteisto/halutaan/'
            , '/feed/uutineet.rss'
            , '/feed/tapahtumat.rss'
            , '/feed/tapahtumat.ics'
        ]

        self.news = News(
            title='Testiuutine'
            , text='Uutineetkin pitää testata'
        )

        self.event = Event(
            title='Testitapahtuma'
            , description='Testikuvaus'
            , location='Testipaikkakunta'
            , starts=timezone.now() + datetime.timedelta(hours=24)
            , ends=timezone.now() + datetime.timedelta(hours=42)
        )

        self.soda = Soda(
            name='Testilimu'
            , price=4.20
            , active=True
        )

        self.news.save()
        self.event.save()
        self.soda.save()

    def test_unicode_methods(self):
        """
        __unicode__ can crash and burn views as well
        if an exception is thrown, so we want to test
        that the models can serialize themselves correctly.

        Just not having an exception is good 'nuf.
        """

        self.news.__unicode__()
        self.event.__unicode__()
        self.soda.__unicode__()

    def test_get_urls(self):
        c = Client()

        for url in self.urls:
            response = c.get(url)
            self.assertEqual(response.status_code, 200)

    def test_get_services(self):
        c = Client()

        response = c.get('/palvelut/')
        self.assertContains(response, 'Testilimu')
        self.assertContains(response, '4,20e')

    def test_get_single_news(self):
        c = Client()

        response = c.get('/uutineet/%d/' % self.news.id)
        self.assertContains(response, 'Testiuutine')
        self.assertContains(response, 'Uutineetkin pitää testata')

    def test_get_single_event(self):
        c = Client()

        response = c.get('/tapahtumat/%d/' % self.event.id)
        self.assertContains(response, 'Testitapahtuma')
        self.assertContains(response, 'Testikuvaus')
        self.assertContains(response, 'Testipaikkakunta')

    def test_get_upcoming_events(self):
        c = Client()

        response = c.get('/tapahtumat/')
        self.assertContains(response, 'Testitapahtuma')
        self.assertContains(response, 'Testikuvaus')
        self.assertContains(response, 'Testipaikkakunta')


class FeedbackTest(TestCase):
    """
    Test leaving feedback via the form.
    """

    def setUp(self):
        self.feedback = {
            'sender': 'Jumal Velho'
            , 'email': 'jumal.velho@example.org'
            , 'message': 'Moi\nTäs Jumal Velho'
        }

    def test_feedback_to_unicode(self):
        feedback = Feedback(**self.feedback)
        feedback.save()
        feedback.__unicode__()

    def test_invalid_feedback(self):
        del self.feedback['message']
        c = Client()
        response = c.post('/palaute/', self.feedback)
        self.assertEqual(response.status_code, 400)

    def test_feedback_sent(self):
        c = Client()
        response = c.post('/palaute/', self.feedback)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Modeemi ry - Palaute verkkosivujen kautta')


class ApplicationViewTest(TestCase):
    """
    Check that mail is sent to users when creating an application.
    Note that you still need valid mail server in addition to this.
    """

    def setUp(self):
        self.application = {
            'email': 'teemu.teekkari@example.org'
            , 'first_name': 'Teemu'
            , 'last_name': 'Teekkari'
            , 'primary_nick': 'teemut'
            , 'secondary_nick': 'teekkarit'
            , 'shell': '/bin/zsh'
            , 'funet_rules_accepted': True
            , 'password': 'testi'
            , 'password_check': 'testi'
        }

    def test_invalid_application(self):
        """
        Test that invalid application is rejected with HTTP status code 400.
        """

        del self.application['first_name']
        c = Client()
        response = c.post('/jaseneksi/', self.application)

        self.assertContains(response
                , 'Tämä kenttä vaaditaan.'
                , status_code=400)

    def test_password_mismatch(self):
        """
        Test that invalid application is rejected with HTTP status code 400.
        """

        self.application['password_check'] = 'eisama'
        c = Client()
        response = c.post('/jaseneksi/', self.application)

        self.assertContains(response
                , 'Salasana ja tarkiste eivät täsmää.'
                , status_code=400)

    def test_application_made(self):
        """
        Test that mail is sent when an application is made.
        """

        c = Client()
        response = c.post('/jaseneksi/', self.application)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject,
                'Modeemi ry - Uusi jäsenhakemus jätetty')
        self.assertEqual(mail.outbox[1].subject,
                'Modeemi ry - Jäsenhakemuksesi lisätiedot')

    def test_reference_number(self):
        c = Client()
        response = c.get('/viitenumero/puuttuvaKayttaja/')
        self.assertEqual(response.status_code, 404)

        del self.application['password']
        del self.application['password_check']
        a = Application(**self.application)
        a.save()

        response = c.get('/viitenumero/%s/' % a.primary_nick)
        self.assertContains(response, 'Viitteenne on %s' % a.bank_reference)


class ApplicationMethodTest(TestCase):
    """
    Test Application model methods.
    """

    def setUp(self):
        self.application = Application(
                first_name='Pekka',
                last_name='Sauron',
                email='pekka.sauron@example.org',
                primary_nick='pekkas',
                secondary_nick='sauronp',
                shell=Application.BASH,
                funet_rules_accepted=True)

        self.application.save()
        self.application.generate_password_hashes(password='pekkaonparas:D')
        self.application.update_bank_reference()

    def test_application_to_unicode(self):
        self.application.__unicode__()

    def test_application_accepted(self):
        application_accepted(self.application)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                'Modeemi ry - Jäsenhakemuksesi on käsitelty')

    def test_application_rejected(self):
        application_rejected(self.application)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                'Modeemi ry - Jäsenhakemuksesi on käsitelty')

    def test_update_bank_reference(self):
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
