# File name: test_integration.py
# Author: Jordan Juravsky
# Date created: 27-08-2018

"""Tests different combinations of command-line usages of buf, ensuring that niche cases involving multiple
functions/buf modules are handled properly. NOTE: these are NOT unit tests (nothing is tested in isolation)."""

from unittest import TestCase, mock
from buf.commands import chemical, recipe, make
from buf import libraries
from buf.main import line


class TestChemical(TestCase):
    """Tests series of command line inputs involving (primarily) buf.commands.chemical"""
    def test_addition_deletion_nicknaming(self):
        """Tests a sequence of additions, deletion, and nicknaming."""
        chemical.reset()

class TestRecipe(TestCase):

    def test_read_write(self):
        with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value={"salt": None, "pepper": None}):

            recipe.reset()

            first_recipe = recipe.Recipe("name", ["300mM"], ["salt"])
            second_recipe = recipe.Recipe("other", ["4M"], ["pepper"])

            correct_dict = {"name": first_recipe, "other": second_recipe}

            with mock.patch("buf.commands.recipe.load_recipes", return_value = {}):

                recipe.add_single_recipe("name", ["300mM"], ["salt"])
                recipe.add_single_recipe("other", ["4M"], ["pepper"])

            recipes = recipe.load_recipes()

            self.assertEqual(len(recipes), len(correct_dict))

            for key, value in correct_dict.items():
                self.assertTrue(key in recipes)
                self.assertEqual(value, recipes[key])