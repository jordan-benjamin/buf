# File name: test_error_messages.py
# Author: Jordan Juravsky
# Date created: 14-08-2018

from buf import error_messages
from inspect import getmembers, isfunction
from unittest import TestCase, mock

class TestErrorMessages(TestCase):
    def test_each_method_prints_and_exits(self):
        with mock.patch("buf.error_messages.print") as mock_print:
            function_tuples = getmembers(error_messages, isfunction)

            for function_name, function_object in function_tuples:
                with self.assertRaises(SystemExit):
                    # TODO: figure out how to access signature of a function, to call each error function properly.
                    function_object() # this will fail often, since almost every function in the module has arguments