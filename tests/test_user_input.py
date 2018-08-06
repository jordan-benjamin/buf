# File name: test_user_input.py
# Author: Jordan Juravsky
# Date created: 06-08-2018

from unittest import mock, TestCase

from buf import user_input

class TestConfirm(TestCase):

    def test_no_reponse(self):

        with mock.patch("buf.user_input.input", side_effect = ["fsd", "fsd", "n"]) as mock_input:
            with self.assertRaises(SystemExit):
                user_input.confirm()

        self.assertEqual(mock_input.call_count, 3)

    def test_yes_response(self):

        with mock.patch("buf.user_input.input", side_effect = ["fsd", "fsd", "y"]) as mock_input:
            user_input.confirm()

        self.assertEqual(mock_input.call_count, 3)