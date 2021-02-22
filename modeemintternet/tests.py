"""
Unit tests for modeemintternet app.
"""

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Permission
from django.core import mail, management
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from passlib.hash import sha256_crypt, sha512_crypt

from modeemintternet.models import (
    Application,
    Feedback,
    Format,
    Membership,
    MembershipFee,
    News,
    Passwd,
    Shadow,
    ShadowFormat,
    Soda,
    UserGroup,
)
from modeemintternet.mailer import application_accepted, application_rejected
from modeemintternet.tasks import remind, deactivate, activate
from modeemintternet.auth import check_password

User = get_user_model()


class ViewGetTest(TestCase):
    def setUp(self):
        poster = User.objects.create(username="ahto.simakuutio")

        self.urls = [
            "/",
            "/ry/",
            "/palvelut/",
            "/jaseneksi/",
            "/laitteisto/",
            "/palaute/",
            "/uutiset/",
            "/ry/saannot/",
            "/ry/rekisteriseloste/",
            "/ry/hallitus/",
            "/ry/yhteystiedot/",
            "/palvelut/backup/",
            "/palvelut/password/",
            "/laitteisto/halutaan/",
            "/feed/uutiset.rss",
            "/feed/uutiset.ics",
        ]

        self.news = News(
            title="Testiuutinen",
            text="Uutisetkin pitää testata",
            location="Testipaikkakunta",
            starts=timezone.now() + timedelta(hours=24),
            ends=timezone.now() + timedelta(hours=42),
            poster=poster,
        )

        self.soda = Soda(name="Testilimu", price=4.20, active=True)

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

        response = c.get("/palvelut/")
        self.assertContains(response, "Testilimu")
        self.assertContains(response, "4,20e")

    def test_get_single_news(self):
        c = Client()

        response = c.get("/uutiset/{}/".format(self.news.id))
        self.assertContains(response, "Testiuutinen")
        self.assertContains(response, "Uutisetkin pitää testata")


class FeedbackTest(TestCase):
    """
    Test leaving feedback via the form.
    """

    def setUp(self):
        self.feedback = {
            "sender": "Jumal Velho",
            "email": "jumal.velho@example.org",
            "message": "Moi\nTäs Jumal Velho",
        }

    def test_feedback_to_unicode(self):
        feedback = Feedback(**self.feedback)
        feedback.save()
        feedback.__str__()

    def test_invalid_feedback(self):
        del self.feedback["message"]
        c = Client()
        response = c.post("/palaute/", self.feedback)
        self.assertEqual(response.status_code, 400)

    def test_feedback_sent(self):
        c = Client()
        response = c.post("/palaute/", self.feedback)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            settings.EMAIL_SUBJECT_PREFIX + "Palaute verkkosivujen kautta",
        )


class ApplicationViewTest(TestCase):
    """
    Check that mail is sent to users when creating an application.
    Note that you still need valid mail server in addition to this.
    """

    def setUp(self):
        self.application = {
            "email": "teemu.teekkari@example.org",
            "first_name": "Teemu",
            "last_name": "Teekkari",
            "municipality": "Tampere",
            "username": "teemut",
            "shell": "/bin/zsh",
            "funet_rules_accepted": True,
            "password": "testisalasana",
            "password_check": "testisalasana",
        }

    def test_invalid_application(self):
        """
        Test that invalid application is rejected with HTTP status code 400.
        """

        del self.application["first_name"]
        c = Client()
        response = c.post("/jaseneksi/", self.application)

        self.assertContains(response, "Tämä kenttä vaaditaan.", status_code=400)

    def test_password_mismatch(self):
        """
        Test that invalid application is rejected with HTTP status code 400.
        """

        self.application["password_check"] = "eisamasalasana"
        c = Client()
        response = c.post("/jaseneksi/", self.application)

        self.assertContains(
            response, "Salasana ja tarkiste eivät täsmää.", status_code=400
        )

    def test_application_made(self):
        """
        Test that mail is sent when an application is made.
        """

        c = Client()
        response = c.post("/jaseneksi/", self.application)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(
            mail.outbox[0].subject,
            settings.EMAIL_SUBJECT_PREFIX + "Uusi jäsenhakemus jätetty",
        )
        self.assertEqual(
            mail.outbox[1].subject,
            settings.EMAIL_SUBJECT_PREFIX + "Jäsenhakemuksesi lisätiedot",
        )


class ApplicationMethodTest(TestCase):
    """
    Test Application model methods.
    """

    def setUp(self):
        UserGroup.objects.get_or_create(groupname="root", gid=1)
        Passwd.objects.get_or_create(
            username="root", uid=1, gid=1, gecos="", home="/root", shell="/bin/bash"
        )

        UserGroup.objects.get_or_create(groupname="modeemi", gid=2)
        UserGroup.objects.get_or_create(groupname="ovi", gid=3)
        Format.objects.get_or_create(format="SHA512")

        self.application = Application(
            first_name="Pekka",
            last_name="Sauron",
            email="pekka.sauron@example.org",
            username="pekkas",
            shell=Application.Shell.BASH,
            funet_rules_accepted=True,
            virtual_key_required=True,
        )

        self.application.save()
        self.application.generate_password_hashes(password="pekkaonparas:D")

    def test_application_to_unicode(self):
        self.application.__str__()

    def test_application_accept(self):
        self.application.accept()

    def test_application_reject(self):
        self.application.reject()

    def test_application_accepted_mailer(self):
        application_accepted(self.application)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            settings.EMAIL_SUBJECT_PREFIX + "Jäsenhakemuksesi on käsitelty",
        )

    def test_application_rejected_mailer(self):
        application_rejected(self.application)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            settings.EMAIL_SUBJECT_PREFIX + "Jäsenhakemuksesi on käsitelty",
        )


class PasswordUpdateViewTest(TestCase):
    def setUp(self):
        self.last_updated = timezone.now()
        self.username = "ahto"
        self.password = "ahdonsalasana"
        self.user = User.objects.create(
            username=self.username, email="ahto.simakuutio@example.com"
        )

        UserGroup.objects.get_or_create(groupname="modeemi", gid=1000)
        passwd, _ = Passwd.objects.get_or_create(
            username="ahto",
            uid=1000,
            gid=1000,
            gecos="",
            home="/home/ahto",
            shell="/bin/bash",
        )
        shadow = Shadow.objects.create(
            username=passwd,
            lastchanged=int(self.last_updated.timestamp()) // 86400,
            min=0,
        )

        Format.objects.get_or_create(format="SHA256")
        Format.objects.get_or_create(format="SHA512")

        for format_ in Format.objects.all():
            hash_ = {
                "SHA512": sha512_crypt.hash(self.password),
                "SHA256": sha256_crypt.hash(self.password),
            }.get(format_.format, None)

            if hash_:
                ShadowFormat.objects.create(
                    username=passwd,
                    format=format_,
                    hash=hash_,
                    last_updated=self.last_updated,
                )

    def test_password_update_unauthenticated_get(self):
        response = self.client.get(reverse("password_update"))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('password_update')}"
        )

    def test_password_update_authenticated_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("password_update"))
        self.assertEqual(200, response.status_code)

    def test_password_update_authenticated_invalid_old_password_post(self):
        self.client.force_login(self.user)
        new_password = "ahtonuusisalasana"
        response = self.client.post(
            reverse("password_update"),
            {
                "password": "vääräahtonvanhasalasana",
                "new_password": "ahtonuusisalasana",
                "new_password_check": "ahtonuusisalasana",
            },
        )
        self.assertContains(response, "Vanha salasana ei ole oikein.", status_code=400)

    def test_password_update_authenticated_invalid_new_password_check_post(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("password_update"),
            {
                "password": self.password,
                "new_password": "ahtonuusisalasana",
                "new_password_check": "ahtonuusisalsasana",
            },
        )
        self.assertContains(
            response, "Salasana ja tarkiste eivät täsmää.", status_code=400
        )

    def test_password_update_submit_authenticated_successful_post(self):
        self.client.force_login(self.user)
        new_password = "ahtonuusisalasana"
        response = self.client.post(
            reverse("password_update"),
            {
                "password": self.password,
                "new_password": new_password,
                "new_password_check": new_password,
            },
        )
        self.assertRedirects(
            response,
            reverse("account_read"),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        # self.assertEqual(302, response.status_code)

        # Old password is gone
        old_password_ok = check_password(username=self.username, password=new_password)
        self.assertFalse(old_password_ok)

        # New password works
        new_password_ok = check_password(username=self.username, password=self.password)
        self.assertTrue(new_password_ok)


class MembershipTest(TestCase):
    """
    Test membership account register_read views.
    """

    def setUp(self):
        self.user = User.objects.create(
            username="ahtosi", email="ahto.simakuutio@example.com"
        )

        self.membership = Membership.objects.create(
            user=self.user, municipality="Tampere", key_virtual=True
        )

        self.fee = MembershipFee.objects.create(year=2011)
        self.membership.fee.add(self.fee)

    def test_view_membership_own_not_logged_in(self):
        response = self.client.get(reverse("account_read"))
        self.assertEqual(302, response.status_code)

    def test_view_membership_own_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_read"))
        self.assertEqual(200, response.status_code)

    def test_view_membership_update_own_not_logged_in(self):
        response = self.client.get(reverse("account_update"))
        self.assertEqual(302, response.status_code)

    def test_view_membership_update_own_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_update"))
        self.assertEqual(200, response.status_code)

    def test_view_membership_update_own_logged_in_post(self):
        self.client.force_login(self.user)

        data = {
            "first_name": "Testi",
            "last_name": "Hehtokuutio",
            "email": "testi.hehtokuutio@example.com",
            "municipality": "Mordor",
        }

        response = self.client.post(reverse("account_update"), data)

        self.assertEqual(302, response.status_code)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, data["first_name"])
        self.assertEqual(self.user.last_name, data["last_name"])
        self.assertEqual(self.user.email, data["email"])
        self.assertEqual(self.user.membership.municipality, data["municipality"])

    def test_view_membership_registry_not_logged_in(self):
        response = self.client.get(reverse("register_read"))
        self.assertEqual(302, response.status_code)

    def test_view_membership_registry_logged_in_without_permission(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("register_read"))
        self.assertEqual(403, response.status_code)

    def test_view_membership_registry_logged_in_with_permission(self):
        permission = Permission.objects.get(codename="view_membership")
        self.user.user_permissions.add(permission)

        self.client.force_login(self.user)
        response = self.client.get(reverse("register_read"))
        self.assertEqual(200, response.status_code)

    def test_view_membership_registry_lists_logged_in_with_permission(self):
        permission = Permission.objects.get(codename="view_membership")
        self.user.user_permissions.add(permission)

        self.client.force_login(self.user)
        response = self.client.get(reverse("register_emails"))
        self.assertEqual(200, response.status_code)

    def test_update_membership_registry(self):
        permission = Permission.objects.get(codename="change_membership")
        self.user.user_permissions.add(permission)

        self.client.force_login(self.user)

        user, _ = User.objects.get_or_create(username="hehtosi")

        response = self.client.get(reverse("register_update", args=(user.username,)))
        self.assertEqual(200, response.status_code)

        data = {
            "first_name": "Testi",
            "last_name": "Hehtokuutio",
            "email": "testi.hehtokuutio@example.com",
            "municipality": "Mordor",
        }

        response = self.client.post(
            reverse("register_update", args=(user.username,)), data
        )

        user.refresh_from_db()
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.membership.municipality, data["municipality"])

        self.assertEqual(302, response.status_code)

    def test_update_membership_fee(self):
        permission = Permission.objects.get(codename="change_membership")
        self.user.user_permissions.add(permission)

        self.client.force_login(self.user)

        response = self.client.get(reverse("register_fees"))
        self.assertEqual(200, response.status_code)

        user_one, _ = User.objects.get_or_create(
            username="hehtosi", email="hehtosi@example.com"
        )
        Membership.objects.get_or_create(user=user_one)

        user_two, _ = User.objects.get_or_create(
            username="simakuu", email="simakuu@example.com", is_active=False
        )
        Membership.objects.get_or_create(user=user_two)

        data = {"year": "2018", "usernames": "hehtosi simakuu"}

        response = self.client.post(reverse("register_fees"), data)
        self.assertEqual(302, response.status_code)
        self.assertTrue(user_one.membership.fee.get(year="2018"))
        self.assertTrue(user_two.membership.fee.get(year="2018"))
        self.assertFalse(user_two.is_active)

        year = datetime.now().year

        data = {"year": str(year), "usernames": "simakuu"}

        response = self.client.post(reverse("register_fees"), data)
        self.assertEqual(302, response.status_code)

        user_two.refresh_from_db()
        self.assertTrue(user_two.membership.fee.get(year=year))
        self.assertTrue(user_two.is_active)

        self.assertEqual(1, len(mail.outbox))
        self.assertIn("Tunnus avattu", mail.outbox[0].subject)
        self.assertIn(user_two.username, mail.outbox[0].body)

    def test_membership_remind(self):
        reminded = remind()
        self.assertEqual(reminded, [self.user.username])
        self.assertEqual(1, len(mail.outbox))
        self.assertIn("Tunnus sulkeutumassa", mail.outbox[0].subject)
        self.assertIn(self.membership.user.username, mail.outbox[0].body)

    def test_membership_remind_command(self):
        management.call_command("remind")
        self.assertEqual(1, len(mail.outbox))
        self.assertIn("Tunnus sulkeutumassa", mail.outbox[0].subject)
        self.assertIn(self.membership.user.username, mail.outbox[0].body)

    def test_membership_remind_paid(self):
        fee = MembershipFee.objects.create(year=datetime.now().year)
        self.membership.fee.add(fee)
        remind()
        self.assertEqual(0, len(mail.outbox))

    def test_membership_deactivate(self):
        deactivated = deactivate()
        self.assertEqual(deactivated, [self.user.username])
        self.assertEqual(1, len(mail.outbox))
        self.assertIn("Tunnus suljettu", mail.outbox[0].subject)
        self.assertIn(self.membership.user.username, mail.outbox[0].body)

    def test_membership_deactivate_command(self):
        management.call_command("deactivate")
        self.assertEqual(1, len(mail.outbox))
        self.assertIn("Tunnus suljettu", mail.outbox[0].subject)
        self.assertIn(self.membership.user.username, mail.outbox[0].body)

    def test_membership_deactivate_paid(self):
        fee = MembershipFee.objects.create(year=datetime.now().year)
        self.membership.fee.add(fee)
        deactivate()
        self.assertEqual(0, len(mail.outbox))

    def test_membership_activate(self):
        self.test_membership_deactivate()
        fee = MembershipFee.objects.create(year=datetime.now().year)
        self.membership.fee.add(fee)

        activated = activate()
        self.assertEqual(activated, [self.user.username])
        self.assertEqual(2, len(mail.outbox))
        self.assertIn("Tunnus avattu", mail.outbox[1].subject)
        self.assertIn(self.membership.user.username, mail.outbox[1].body)

    def test_membership_activate_command(self):
        self.test_membership_deactivate()
        fee = MembershipFee.objects.create(year=datetime.now().year)
        self.membership.fee.add(fee)

        management.call_command("activate")
        self.assertEqual(2, len(mail.outbox))
        self.assertIn("Tunnus avattu", mail.outbox[1].subject)
        self.assertIn(self.membership.user.username, mail.outbox[1].body)
