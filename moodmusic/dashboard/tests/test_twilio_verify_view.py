from django.urls import reverse
from django.test import TestCase

from moodmusic.users.tests.factories import UserFactory


class TestVerifiedConfirmationView(TestCase):
    def setUp(self):
        # Make a pretend user and log them in
        self.user = UserFactory.build()
        self.user.save()
        self.client.force_login(self.user)

    def test_not_verified(self):
        """Assert user is redirected if they are not verified"""
        response = self.client.get(reverse("dashboard:verified"))
        self.assertEqual(response.status_code, 302)

    def test_verified(self):
        """Assert verified user gets the page as expected"""
        # Set verified as True
        session = self.client.session
        session["is_verified"] = [True]
        session.save()
        # Get the verified page
        response = self.client.get(reverse("dashboard:verified"))
        self.assertEqual(response.status_code, 200)

    def test_not_logged_in(self):
        """Assert user is redirected from this page if not logged in"""
        # Log out
        self.client.logout()
        # Get the verified page
        response = self.client.get(reverse("dashboard:verified"))
        self.assertEqual(response.status_code, 302)
