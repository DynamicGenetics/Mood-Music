import pytest

from hypothesis.extra.django import TestCase
from hypothesis import given, assume
from hypothesis import strategies as st

from moodmusic.users.forms import CustomSignupForm
from moodmusic.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUserCreationForm(TestCase):
    def test_clean_email(self):
        """Check complete form is valid"""

        # A user with proto_user params does not exist yet.
        proto_user = UserFactory.build()

        user = {
            "email": proto_user.email,
            "password1": proto_user._password,
            "password2": proto_user._password,
            "seen_information": True,
            "voluntary_participation": True,
            "data_unwithdrawable": True,
            "data_collected": True,
            "confidentiality": True,
            "data_access": True,
            "data_stored_longterm": True,
            "could_be_reused": True,
            "breaking_confidentiality": True,
            "consent_granted": True,
        }

        form = CustomSignupForm(user)

        assert form.is_valid()
        assert form.clean_email() == proto_user.email

    @given(
        a=st.booleans(),
        b=st.booleans(),
        c=st.booleans(),
        d=st.booleans(),
        e=st.booleans(),
        f=st.booleans(),
        g=st.booleans(),
        h=st.booleans(),
        i=st.booleans(),
        j=st.booleans(),
    )
    def test_consent_flags(self, a, b, c, d, e, f, g, h, i, j):
        """Check incomplete consent boxes makes form invalid"""
        # Tell Hypothesis that when all true is an exception
        assume(
            not (
                a is True
                and b is True
                and c is True
                and d is True
                and e is True
                and f is True
                and g is True
                and h is True
                and i is True
                and j is True
            )
        )

        # Build a pretend user
        proto_user = UserFactory.build()

        # Set up user object
        user = {
            "email": proto_user.email,
            "password1": proto_user._password,
            "password2": proto_user._password,
            "seen_information": a,
            "voluntary_participation": b,
            "data_unwithdrawable": c,
            "data_collected": d,
            "confidentiality": e,
            "data_access": f,
            "data_stored_longterm": g,
            "could_be_reused": h,
            "breaking_confidentiality": i,
            "consent_granted": j,
        }

        form = CustomSignupForm(user)

        assert not form.is_valid()

    def test_bristol_email(self):
        """Check non bristol email does not work"""
        proto_user = UserFactory.build()

        user = {
            "email": "hello@example.co.uk",
            "password1": proto_user._password,
            "password2": proto_user._password,
            "seen_information": True,
            "voluntary_participation": True,
            "data_unwithdrawable": True,
            "data_collected": True,
            "confidentiality": True,
            "data_access": True,
            "data_stored_longterm": True,
            "could_be_reused": True,
            "breaking_confidentiality": True,
            "consent_granted": True,
        }

        form = CustomSignupForm(user)

        assert not form.is_valid()
