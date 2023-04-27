"""
Tests for RepApp.
"""
from hashlib import sha256
from datetime import datetime, timedelta

import django.utils.timezone

from django.test import TestCase
from django.test import Client
from django.urls import reverse

from .backends import OneTimeLoginBackend, EmailBackend, create_repapp_user
from .models import (OneTimeLogin, CustomUser, Cafe, Organisator, Reparateur)


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


class BackendsTest(TestCase):
    """
    Test for backend utility functions.
    """

    def setUp(self):
        organisator = Organisator(
            name="Organisator Name",
            mail="orga@example.com",
        )
        organisator.save()
        self.organisator = organisator

        reparateur = Reparateur(
            name="Reparateur Name",
            mail="repa@example.com",
        )
        reparateur.save()
        self.reparateur = reparateur

    def test_create_reparateur(self):
        """
        Ensure that a new reparateur is created.
        """
        user = CustomUser(
            username="Other Reparateur",
            email="repa2@example.com",
        )
        user.save()
        create_repapp_user(user)

        reparateur = Reparateur.objects.filter(mail=user.email).first()
        self.assertIsNotNone(reparateur)
        self.assertEqual(reparateur.name, user.username)

    def test_update_reparateur(self):
        """
        Ensure that the reparateur name gets updated.
        """
        user = CustomUser(
            username="First Reparateur",
            email="repa@example.com",
        )
        user.save()
        create_repapp_user(user)

        reparateur = Reparateur.objects.filter(mail=user.email).first()
        self.assertIsNotNone(reparateur)
        self.assertEqual(reparateur.name, user.username)

    def test_update_organisator(self):
        """
        Ensure that the organisator name gets updated.
        """
        user = CustomUser(
            username="The Organisator",
            email="orga@example.com",
        )
        user.save()
        create_repapp_user(user)

        organisator = Organisator.objects.filter(mail=user.email).first()
        self.assertIsNotNone(organisator)
        self.assertEqual(organisator.name, user.username)


class FormsTest(TestCase):
    """
    Test for RepApp form features.
    """

    fixtures = ["cafe-data.json"]

    def test_from_protection(self):
        client = Client(enforce_csrf_checks=True)
        response = client.get(reverse('register_device', kwargs={
            'cafe': 1,
        }))
        # ensure honeypot field is available
        self.assertContains(
            response, 'type="text" name="accept_agb" style="display:none"')
        # ensure csrf is available
        self.assertContains(response, 'csrfmiddlewaretoken')


class ViewsTest(TestCase):
    """
    Test for RepApp views.
    """
    fixtures = ["cafe-data.json"]

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

        user = CustomUser(
            username="ATestUser",
            email="testuser@example.com",
        )
        user.set_password("aTestPassword")
        user.save()
        self.user = user

        reparateur = Reparateur(
            name="ATestUser",
            mail="testuser@example.com"
        )
        reparateur.save()
        self.reparateur = reparateur

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

    def test_register_device(self):
        """
        Test register device view
        """
        client = Client(enforce_csrf_checks=True)
        response = client.get(reverse('register_device', kwargs={
            'cafe': 1,
        }))

        self.assertEqual(response.status_code, 200)

        # ensure all required fields are displayed
        self.assertContains(response, "eMail Adresse")
        self.assertContains(response, "Art des Geräts")
        self.assertContains(response, "Hersteller")
        self.assertContains(response, "Fehlerbeschreibung")
        self.assertContains(response, "Foto vom Gerät")
        self.assertContains(response, "Foto vom Typenschild")
        self.assertContains(response, "Folgetermin")
        self.assertContains(response, "Informationen zur Reparaturabwicklung")
        self.assertContains(response, "Datenschutz")
        # ensure security fields are contained
        self.assertContains(
            response, 'type="text" name="accept_agb" style="display:none"')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_member_login(self):
        """
        Test member login view
        """
        client = Client(enforce_csrf_checks=True)
        response = client.get(reverse('member_login'))

        self.assertEqual(response.status_code, 200)

        # ensure OIDC link is displayed
        self.assertContains(response, "Anmelden mit Makes-Hacks-Hip")

        client.login(username="testuser@example.com", password="aTestPassword")
        response = client.get(reverse('member_login'))
        self.assertEqual(response.status_code, 200)

        # ensure logout button is displayed
        self.assertContains(response, "Abmelden")
        # ensure user is displayed
        self.assertContains(response, "testuser@example.com")
