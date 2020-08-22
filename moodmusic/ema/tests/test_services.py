# import pytest

from moodmusic.ema.services import is_valid

# ----------------
# REQUIRED TESTS
# ----------------
# Manage a phone number that does not exist
# Test is_valid both true and false
# Test


def test_is_valid():
    assert is_valid("hello") is False
    assert is_valid("10") is True
    assert is_valid("3lf") is False
