from django.urls import reverse
from django.test import TestCase

from moodmusic.users.tests.factories import UserFactory


class TestStaticViewsLoggedIn(TestCase):
    def setUp(self):
        # Make a pretend user and log them in
        user = UserFactory.build()
        user.save()
        self.client.force_login(user)

    def test_dashboard_view(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)

    def test_thanks_view(self):
        response = self.client.get(reverse("dashboard:thanks"))
        self.assertEqual(response.status_code, 200)

    def test_spotify_connect_view(self):
        response = self.client.get(reverse("dashboard:spotify"))
        self.assertEqual(response.status_code, 200)

    def test_mobile_guide_view(self):
        response = self.client.get(reverse("dashboard:spotify"))
        self.assertEqual(response.status_code, 200)


class TestStaticViewsLoggedOut(TestCase):
    """Assert that when no user is logged in then 302 (redirect to
    the login page) status code is passed."""

    def test_dashboard_view(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 302)

    def test_thanks_view(self):
        response = self.client.get(reverse("dashboard:thanks"))
        self.assertEqual(response.status_code, 302)

    def test_spotify_connect_view(self):
        response = self.client.get(reverse("dashboard:spotify"))
        self.assertEqual(response.status_code, 302)

    def test_mobile_guide_view(self):
        response = self.client.get(reverse("dashboard:spotify"))
        self.assertEqual(response.status_code, 302)
