# File name: test_error_messages.py
# Author: Jordan Juravsky
# Date created: 14-08-2018

"""Tests buf.error_messages."""

from buf import error_messages
from inspect import getmembers, isfunction, signature
from unittest import TestCase, mock

class TestErrorMessages(TestCase):
    """Wrapper class that tests the error_messages module as a whole."""

    def test_each_method_prints_and_exits(self):
        """Verifies that each method in the module prints out an error messages to the user and raises SysExit (exits the program)."""
        with mock.patch("buf.error_messages.print") as mock_print:
            function_tuples = getmembers(error_messages, isfunction)

            for function_name, function_object in function_tuples:

                num_parameters = len(signature(function_object).parameters)

                # Since all the functions are doing with their arguments is printing them out (and sometimes, in the case
                # of arguments that are line numbers, incrementing the argument by one before printing it out),
                # simply replacing each argument with an integer should work fine.
                dummy_parameters = [1 for _ in range(num_parameters)]

                with self.assertRaises(SystemExit):
                    function_object(*dummy_parameters)

                mock_print.assert_called()
                mock_print.reset_mock()