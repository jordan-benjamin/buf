# File name: test_command_line.py
# Author: Jordan Juravsky
# Date created: 14-08-2018

"""Testing the full usage of buf from the command line."""

import unittest
from unittest import mock, TestCase
from buf.main import line, reset
import tabulate
from buf import error_messages

class ChemicalTests(TestCase):
    """Testing using 'buf chemical' from the command line."""

    def test_single_chemical_addition(self):
        with mock.patch("buf.commands.chemical.add_single_chemical") as mock_add:
            reset()
            line("buf chemical -a 58.44 NaCl salt")
            mock_add.assert_called_with("58.44", ["NaCl", "salt"])

    def test_add_chemicals_from_file(self):
        with mock.patch("buf.commands.chemical.add_chemicals_from_file") as mock_add:
            reset()
            line("buf chemical -a file.txt")
            mock_add.assert_called_with("file.txt")

    def test_nickname_chemical(self):
        with mock.patch("buf.commands.chemical.nickname_chemical") as mock_nickname:
            reset()
            line("buf chemical -n NaCl salt")
            mock_nickname.assert_called_with("NaCl", ["salt"])

    def test_chemical_deletion(self):
        with mock.patch("buf.commands.chemical.delete_chemical") as mock_deletion:
            reset()
            line("buf chemical -d NaCl")
            mock_deletion.assert_called_with("NaCl", prompt_for_confirmation = True, complete_deletion = False)

            line("buf chemical -d NaCl --confirm")
            mock_deletion.assert_called_with("NaCl", prompt_for_confirmation=False, complete_deletion=False)

            line("buf chemical -d NaCl --complete")
            mock_deletion.assert_called_with("NaCl", prompt_for_confirmation=True, complete_deletion=True)

    def test_display_chemical_information(self):
        with mock.patch("buf.commands.chemical.display_chemical_information") as mock_display:
            reset()
            line("buf chemical NaCl")
            mock_display.assert_called_with("NaCl")

    def test_display_chemical_library(self):
        with mock.patch("buf.commands.chemical.display_chemical_library") as mock_display:
            reset()
            line("buf chemical")
            mock_display.assert_called()

class RecipeTests(TestCase):
    """Testing using 'buf recipe' from the command line."""

    def test_single_recipe_addition(self):
        with mock.patch("buf.commands.recipe.add_single_recipe") as mock_add:
            reset()
            line("buf recipe -a my_recipe 300mM salt 10% glycerol")
            mock_add.assert_called_with("my_recipe", ["300mM", "10%"], ["salt", "glycerol"])

    def test_add_recipes_from_file(self):
        with mock.patch("buf.commands.recipe.add_recipes_from_file") as mock_add:
            reset()
            line("buf recipe -a file.txt")
            mock_add.assert_called_with("file.txt")

    def test_recipe_deletion(self):
        with mock.patch("buf.commands.recipe.delete_recipe") as mock_deletion:
            reset()
            line("buf recipe -d my_recipe")
            mock_deletion.assert_called_with("my_recipe", prompt_for_confirmation = True)

            line("buf recipe -d my_recipe --confirm")
            mock_deletion.assert_called_with("my_recipe", prompt_for_confirmation = False)

    def test_display_recipe_information(self):
        with mock.patch("buf.commands.recipe.display_recipe_information") as mock_display:
            reset()
            line("buf recipe my_recipe")
            mock_display.assert_called_with("my_recipe")

    def test_display_recipe_library(self):
        with mock.patch("buf.commands.recipe.display_recipe_library") as mock_display:
            reset()
            line("buf recipe")
            mock_display.assert_called()

if __name__ == '__main__':
    unittest.main()