"""
Unit tests for modeemintternet app.
"""

import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from modeemintternet.models import Application, Membership, MembershipFee, Feedback, News, Soda
from modeemintternet.mailer import application_accepted, application_rejected

User = get_user_model()


class ViewGetTest(TestCase):
    def setUp(self):
        self.urls = [
            '/'
            , '/ry/'
            , '/palvelut/'
            , '/jaseneksi/'
            , '/laitteisto/'
            , '/palaute/'
            , '/uutiset/'
            , '/ry/saannot/'
            , '/ry/rekisteriseloste/'
            , '/ry/hallitus/'
            , '/ry/yhteystiedot/'
            , '/palvelut/backup/'
            , '/palvelut/password/'
            , '/laitteisto/halutaan/'
            , '/feed/uutiset.rss'
            , '/feed/uutiset.ics'
        ]

        self.news = News(
            title='Testiuutinen'
            , text='Uutisetkin pitää testata'
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
        self.soda.save()

    def test_unicode_methods(self):
        """
        __str__ can crash and burn views as well
        if an exception is thrown, so we want to test
        that the models can serialize themselves correctly.

        Just not having an exception is good 'nuf.
        """

        self.news.__str__()
        self.soda.__str__()

    def test_get_urls(self):
        c = Client()

        for url in self.urls:
            with self.subTest(url):
                response = c.get(url)
                self.assertEqual(response.status_code, 200)

    def test_get_services(self):
        c = Client()

        response = c.get('/palvelut/')
        self.assertContains(response, 'Testilimu')
        self.assertContains(response, '4,20e')

    def test_get_single_news(self):
        c = Client()

        response = c.get('/uutiset/{}/'.format(self.news.id))
        self.assertContains(response, 'Testiuutinen')
        self.assertContains(response, 'Uutisetkin pitää testata')


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
        feedback.__str__()

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
        self.assertEqual(mail.outbox[0].subject,
                         settings.EMAIL_SUBJECT_PREFIX + 'Palaute verkkosivujen kautta')


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
            , 'username': 'teemut'
            , 'secondary_nick': 'teekkarit'
            , 'shell': '/bin/zsh'
            , 'funet_rules_accepted': True
            , 'password': 'testisalasana'
            , 'password_check': 'testisalasana'
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

        self.application['password_check'] = 'eisamasalasana'
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
                settings.EMAIL_SUBJECT_PREFIX + 'Uusi jäsenhakemus jätetty')
        self.assertEqual(mail.outbox[1].subject,
                settings.EMAIL_SUBJECT_PREFIX + 'Jäsenhakemuksesi lisätiedot')


class ApplicationMethodTest(TestCase):
    """
    Test Application model methods.
    """

    def setUp(self):
        self.application = Application(
                first_name='Pekka',
                last_name='Sauron',
                email='pekka.sauron@example.org',
                username='pekkas',
                secondary_nick='sauronp',
                shell=Application.Shell.BASH,
                funet_rules_accepted=True)

        self.application.save()
        self.application.generate_password_hashes(password='pekkaonparas:D')

    def test_application_to_unicode(self):
        self.application.__str__()

    def test_application_accepted(self):
        application_accepted(self.application)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                settings.EMAIL_SUBJECT_PREFIX + 'Jäsenhakemuksesi on käsitelty')

    def test_application_rejected(self):
        application_rejected(self.application)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                settings.EMAIL_SUBJECT_PREFIX + 'Jäsenhakemuksesi on käsitelty')


class MembershipTest(TestCase):
    """
    Test membership account_registry views.
    """

    def setUp(self):
        self.user = User.objects.create(
            username='ahtosi',
            email='ahto.simakuutio@example.com',
        )

        self.membership = Membership.objects.create(
            user=self.user,
            city='Tampere',
            key_virtual=True,
        )

        self.fee = MembershipFee.objects.create(year=2011)
        self.membership.fee.add(self.fee)

    def test_view_membership_own_not_logged_in(self):
        response = self.client.get(reverse('kayttajatiedot'))
        self.assertEqual(302, response.status_code)

    def test_view_membership_own_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('kayttajatiedot'))
        self.assertEqual(200, response.status_code)

    def test_view_membership_update_own_not_logged_in(self):
        response = self.client.get(reverse('kayttajatiedot_paivita'))
        self.assertEqual(302, response.status_code)

    def test_view_membership_update_own_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('kayttajatiedot_paivita'))
        self.assertEqual(200, response.status_code)

    def test_view_membership_update_own_logged_in_post(self):
        self.client.force_login(self.user)

        data = {
            'first_name': 'Testi',
            'last_name': 'Hehtokuutio',
            'email': 'testi.hehtokuutio@example.com',
            'city': 'Mordor',
        }

        response = self.client.post(reverse('kayttajatiedot_paivita'), data)

        self.assertEqual(302, response.status_code)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, data['first_name'])
        self.assertEqual(self.user.last_name, data['last_name'])
        self.assertEqual(self.user.email, data['email'])
        self.assertEqual(self.user.membership.city, data['city'])

    def test_view_membership_registry_not_logged_in(self):
        response = self.client.get(reverse('kayttajarekisteri'))
        self.assertEqual(302, response.status_code)

    def test_view_membership_registry_logged_in_without_permission(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('kayttajarekisteri'))
        self.assertEqual(403, response.status_code)

    def test_view_membership_registry_logged_in_with_permission(self):
        permission = Permission.objects.get(codename='view_membership')
        self.user.user_permissions.add(permission)

        self.client.force_login(self.user)
        response = self.client.get(reverse('kayttajarekisteri'))
        self.assertEqual(200, response.status_code)

    def test_view_membership_registry_lists_logged_in_with_permission(self):
        permission = Permission.objects.get(codename='view_membership')
        self.user.user_permissions.add(permission)

        self.client.force_login(self.user)
        response = self.client.get(reverse('kayttajarekisteri_listat'))
        self.assertEqual(200, response.status_code)

    def test_update_membership_registry(self):
        permission = Permission.objects.get(codename='change_membership')
        self.user.user_permissions.add(permission)

        self.client.force_login(self.user)

        user, _ = User.objects.get_or_create(username='hehtosi')

        response = self.client.get(reverse('kayttajarekisteri_paivita', args=(user.username, )))
        self.assertEqual(200, response.status_code)

        data = {
            'first_name': 'Testi',
            'last_name': 'Hehtokuutio',
            'email': 'testi.hehtokuutio@example.com',
            'city': 'Mordor',
        }

        response = self.client.post(reverse('kayttajarekisteri_paivita', args=(user.username, )), data)

        user.refresh_from_db()
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.membership.city, data['city'])

        self.assertEqual(302, response.status_code)

    def test_update_membership_fee(self):
        permission = Permission.objects.get(codename='change_membership')
        self.user.user_permissions.add(permission)

        self.client.force_login(self.user)

        response = self.client.get(reverse('kayttajarekisteri_jasenmaksut'))
        self.assertEqual(200, response.status_code)

        user_one, _ = User.objects.get_or_create(username='hehtosi')
        user_two, _ = User.objects.get_or_create(username='simakuu')

        data = {
            'year': '2018',
            'usernames': 'hehtosi simakuu',
        }

        response = self.client.post(reverse('kayttajarekisteri_jasenmaksut'), data)
        self.assertEqual(302, response.status_code)
        self.assertTrue(user_one.membership.fee.get(year='2018'))
        self.assertTrue(user_two.membership.fee.get(year='2018'))

        data = {
            'year': '2019',
            'usernames': 'simakuu',
        }

        response = self.client.post(reverse('kayttajarekisteri_jasenmaksut'), data)
        self.assertEqual(302, response.status_code)
        self.assertTrue(user_two.membership.fee.get(year='2019'))
