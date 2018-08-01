# File name: test_recipe.py
# Author: Jordan Juravsky
# Date created: 31-07-2018

from unittest import mock, TestCase

from tempfile import NamedTemporaryFile

if __name__ == '__main__':
    from ..commands import recipe
else:
    from buf.commands import recipe

class SplitConcentrationTest(TestCase):
    def test_correct_split(self):
        for quantity in ["100", "1.0", "2343.5", ".1", "10."]:
            for unit in ["M", "L", "mM", ""]:
                test_string = str(quantity)+unit
                returned_quantity, returned_unit = recipe.split_concentration(test_string)
                self.assertEqual(quantity, returned_quantity)
                self.assertEqual(unit, returned_unit)

class RecipeTest(TestCase):
    def test_existing_chemical_check(self):

        with mock.patch("buf.commands.recipe.exit") as mock_exit:
            with mock.patch("buf.commands.recipe.print") as mock_print:
                # Testing the code stops if no matching chemical
                with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value={}):
                    recipe.make_safe_recipe("boop", ["300mM"], ["Salt"])
                    mock_exit.assert_called()
                    mock_print.assert_called()

                mock_exit.reset_mock()
                mock_print.reset_mock()

                # Testing the code doesn't stop if the chemicals do exist.
                with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value={"salt" : None}):
                    recipe.make_safe_recipe("boop", ["300mM"], ["salt"])
                    mock_exit.assert_not_called()
                    mock_print.assert_not_called()


    def test_unit_validity(self):
        with mock.patch("buf.commands.recipe.exit") as mock_exit:
            with mock.patch("buf.commands.recipe.print") as mock_print:
                with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value={"salt" : None}):
                    # Testing valid units.
                    for unit in ["M", "L", "ug"]:
                        recipe.make_safe_recipe("name", ["123" + unit], ["salt"])
                        mock_print.assert_not_called()
                        mock_exit.assert_not_called()
                        mock_exit.reset_mock()
                        mock_print.reset_mock()

                    # Testing invalid units.
                    for unit in ["", "invalid", "inval1d_w1th_numb3rs"]:
                        recipe.make_safe_recipe("name", ["123" + unit], ["salt"])
                        mock_print.assert_called()
                        mock_exit.assert_called()
                        mock_exit.reset_mock()
                        mock_print.reset_mock()

    def test_quantity_validity(self):
        with mock.patch("buf.commands.recipe.exit") as mock_exit:
            with mock.patch("buf.commands.recipe.print") as mock_print:
                with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value={"salt": None}):

                    # Testing valid quantities.
                    for quantity in ["100", "100.1", "0.1", ".1", "10."]:
                        recipe.make_safe_recipe("name", [quantity + "M"], ["salt"])
                        mock_print.assert_not_called()
                        mock_exit.assert_not_called()
                        mock_exit.reset_mock()
                        mock_print.reset_mock()

                    # Testing invalid quantities.
                    # TODO: negative numbers and zero?
                    for quantity in [""]:
                        recipe.make_safe_recipe("name", [quantity + "L"], ["salt"])
                        mock_print.assert_called()
                        mock_exit.assert_called()
                        mock_exit.reset_mock()
                        mock_print.reset_mock()

    def test_string_cast(self):
        with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value={"salt": None, "pepper" : None}):
            test_recipe = recipe.Recipe("name", ["300mM", "4L"], ["salt", "pepper"])
            self.assertEqual(str(test_recipe), "name 300mM salt 4L pepper")

    # TODO: check two recipes with identical ingredients and concentrations, but in different orders.
    def equals_check(self):
        with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value={"salt": None, "pepper": None}):
            first_recipe = recipe.Recipe("name", ["300mM"], ["salt"])
            second_recipe = recipe.Recipe("name", ["300mM"], ["salt"])
            third_recipe = recipe.Recipe("name2", ["300mM"], ["salt"])
            fourth_recipe = recipe.Recipe("name", ["400mM"], ["salt"])
            fifth_recipe = recipe.Recipe("name", ["300M"], ["salt"])
            sixth_recipe = recipe.Recipe("name", ["300mM"], ["pepper"])

            self.assertEqual(first_recipe, second_recipe)
            self.assertNotEqual(first_recipe, third_recipe)
            self.assertNotEqual(first_recipe, fourth_recipe)
            self.assertNotEqual(first_recipe, fifth_recipe)
            self.assertNotEqual(first_recipe, sixth_recipe)


class IntegratedTests(TestCase):
    # TODO: research whether two dictionaries a = {1: object_a} and b = {1: object_b} are equal if object_a == object_b as defined in __eq__
    def test_read_write(self):
        with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value={"salt": None, "pepper": None}):

            tmp_file = NamedTemporaryFile()
            with mock.patch("buf.commands.recipe.recipe_library_file", tmp_file.name):

                first_recipe = recipe.Recipe("name", ["300mM"], ["salt"])
                second_recipe = recipe.Recipe("other", ["4M"], ["pepper"])

                correct_dict = {"name": first_recipe, "other": second_recipe}

                with mock.patch("buf.commands.recipe.load_recipes", return_value = {}):

                    recipe.add_recipe("name", ["300mM"], ["salt"])
                    recipe.add_recipe("other", ["4M"], ["pepper"])

                recipes = recipe.load_recipes()

                self.assertEqual(len(recipes), len(correct_dict))

                for key, value in correct_dict.items():
                    self.assertTrue(key in recipes)
                    self.assertEqual(value, recipes[key])