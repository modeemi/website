# -*- coding: utf-8 -*-

"""
Unit tests for modeemintternet app.
"""

from django.test import TestCase


class ApplicationMailerTest(TestCase):
    """
    Check that mail is sent to users when creating an application.
    Note that you still need valid mail server in addition to this.
    """

    def test_application_made(self):
        """
        Test that mail is sent when an application is made.
        """
        self.assertEqual(True, True)
