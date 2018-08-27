# File name: test_user_input.py
# Author: Jordan Juravsky
# Date created: 06-08-2018

"""Tests the buf.user_input module."""

from unittest import mock, TestCase
from buf import user_input

class TestConfirm(TestCase):
    """Tests user_input.confirm."""

    def test_no_response(self):
        """Tests that the function raises SystemExit when a 'n' is entered."""

        # The 'fsd' dummy entries exist to check that if an input is invalid, the function asks the
        # user to enter input again.
        with mock.patch("buf.user_input.input", side_effect = ["fsd", "fsd", "n"]) as mock_input:
            with self.assertRaises(SystemExit):
                user_input.confirm()

        self.assertEqual(mock_input.call_count, 3)

    def test_yes_response(self):
        """Tests that the function ends (i.e. does nothing / lets the rest of the code progress') if the user \
        inputs 'y'."""

        with mock.patch("buf.user_input.input", side_effect = ["fsd", "fsd", "y"]) as mock_input:
            user_input.confirm()

        self.assertEqual(mock_input.call_count, 3)