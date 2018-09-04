# File name: test_help.py
# Author: Jordan Juravsky
# Date created: 14-08-2018

"""Tests the buf.commands.help module."""

from unittest import mock, TestCase
import unittest
from buf import commands
from inspect import getmembers, ismodule
from buf.commands import help

class TestHelp(TestCase):
    """Wrapper class for testing the entire module."""

    def test_invalid_name_catch(self):
        """Tests that calling 'buf help' with an invalid module name will raise the appropriate error."""
        with mock.patch("buf.commands.help.error_messages.subcommand_not_found", side_effect = SystemExit) as mock_error:
            test_options_dict = {"<subcommand_name>": "unknown_module"}
            with self.assertRaises(SystemExit):
                help.help(test_options_dict)
                mock_error.assert_called_with("unknown_module")


    def test_module_instructions_print(self):
        """Tests that a module's 'instructions' docstring is printed when the modules name is called with help."""
        module_tuples = getmembers(commands, ismodule)

        with mock.patch("buf.commands.help.print") as mock_print:
            for module_name, module in module_tuples:
                test_options_dict = {"<subcommand_name>": module_name}
                help.help(test_options_dict)
                mock_print.assert_called_with(module.instructions)
                mock_print.reset_mock()

    def test_general_help_docstring_print(self):
        """Tests that help.general_help_docstring is printed when 'buf help' is called.'"""
        with mock.patch("buf.commands.help.print") as mock_print:
            options_dict = {"<subcommand_name>" : None}
            help.help(options_dict)
            mock_print.assert_called_with(help.general_help_docstring)

if __name__ == '__main__':
    unittest.main()