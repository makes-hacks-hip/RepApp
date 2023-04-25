"""
Tests for RepApp.
"""
from hashlib import sha256
from datetime import datetime, timedelta

import django.utils.timezone

from django.test import TestCase
from django.test import Client
from django.urls import reverse

from .backends import OneTimeLoginBackend, EmailBackend
from .models import OneTimeLogin, CustomUser, Cafe


class OneTimeLoginTest(TestCase):
    """
    Tests for the one time login feature.
    """

    def setUp(self):
        user = CustomUser(
            email="user@example.com",
        )
        user.save()
        self.user = user

        secret_hash = sha256("LetMeIn".encode('utf-8')).hexdigest()
        otl = OneTimeLogin(
            secret=secret_hash,
            user=user,
            url="/test/url",
        )
        otl.save()
        self.otl = otl

    def test_allowed_one_time_login(self):
        """
        Test that one time login is allowed.
        """
        backend = OneTimeLoginBackend()
        result = backend.authenticate(None, self.otl.secret, None)

        self.assertEqual(result, self.user)

    def test_unknown_one_time_login(self):
        """
        Test that one time login is not allowed for unknown secret.
        """

        backend = OneTimeLoginBackend()
        result = backend.authenticate(None, "other phrase", None)

        self.assertEqual(result, None)


class EmailLoginTest(TestCase):
    """
    Tests for the one time login feature.
    """

    def setUp(self):
        user = CustomUser(
            email="user@example.com"
        )
        user.set_password("aPassword")
        user.save()
        self.user = user

    def test_allowed_email_login(self):
        """
        Test that email login is allowed.
        """
        backend = EmailBackend()
        result = backend.authenticate(None, self.user.email, "aPassword")

        self.assertEqual(result, self.user)

    def test_unknown_email_login(self):
        """
        Test that email login is not allowed for unknown user.
        """

        backend = EmailBackend()
        result = backend.authenticate(
            None, "other@example.com", "somePassword")

        self.assertEqual(result, None)

    def test_wrong_password_login(self):
        """
        Test that email login is not allowed for wrong password.
        """

        backend = EmailBackend()
        result = backend.authenticate(
            None, self.user.email, "wrongPassword")

        self.assertEqual(result, None)


class UtilsTest(TestCase):
    """
    Test for utility functions.
    """
    pass


class ViewsTest(TestCase):
    """
    Test for RepApp views.
    """

    def setUp(self):
        cafe = Cafe(location="neuer Ort", address="neue Adresse",
                    event_date=django.utils.timezone.now())
        cafe.save()
        self.cafe = cafe

        date = datetime.now() - timedelta(days=7)
        old_cafe = Cafe(location="alter Ort", address="alte Adresse",
                        event_date=date)
        old_cafe.save()
        self.old_cafe = old_cafe

    def test_index(self):
        """
        Test index page.
        """
        client = Client(enforce_csrf_checks=True)
        response = client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

        # ensure future cafe is displayed
        self.assertContains(response, self.cafe.location)
        self.assertContains(response, self.cafe.address)

        # ensure old cafe is not displayed
        self.assertNotContains(response, self.old_cafe.location)
        self.assertNotContains(response, self.old_cafe.address)
