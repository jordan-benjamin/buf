# File name: test_recipe.py
# Author: Jordan Juravsky
# Date created: 31-07-2018

"""Tests buf.commands.recipe."""

from unittest import mock, TestCase

from tempfile import NamedTemporaryFile

from io import StringIO


from buf.commands import recipe


class TestMakeSafeRecipe(TestCase):
    """Tests recipe.make_safe_recipe (and recipe.assert_recipe_validity by proxy, since the former is simply \
    a wrapper for the latter, as make_safe_recipe simply returns the Recipe type-checked by assert_recipe_validity)."""

    def test_spaces_in_name(self):
        """Tests that the function checks that the recipe name does not contain spaces."""
        with mock.patch("buf.commands.recipe.load_recipes", return_value = {}):
            with self.assertRaises(SystemExit):
                 recipe.make_safe_recipe("contains spaces", ["10%"], ["glycerol"])


    def test_existing_chemical_check(self):
        """Tests that the function checks that the chemicals specified in the recipe exist in the chemical library, \
        if their concentration is specified in molar."""

        with mock.patch("buf.commands.recipe.print") as mock_print:
            # Testing the code stops if a chemical's concentration is specified in molar, but the chemical name cannot be found
            # in the chemical library.
            with self.assertRaises(SystemExit):
                recipe.make_safe_recipe("boop", ["300mM"], ["Salt"], chemical_library= {}, recipe_library={})
                mock_print.assert_called()

            mock_print.reset_mock()

            # Verifies that a chemical is only checked to exist in the chemical library if concentration is
            # specified in molar (e.g. here, glycerol is not in the chemical library, yet it does not matter since its
            # concentration is specified in % volume).
            recipe.make_safe_recipe("boop", ["300mM", "10%"], ["salt", "glycerol"], chemical_library={"salt" : None}, recipe_library= {})
            mock_print.assert_not_called()


    def test_unit_validity(self):
        """Tests that the function checks that all concentration values have valid units."""
        with mock.patch("buf.commands.recipe.print") as mock_print:
            # Testing valid units.
            for unit in ["M", "L", "ug"]:
                recipe.make_safe_recipe("name", ["123" + unit], ["salt"], chemical_library={"salt" : None}, recipe_library={})
                mock_print.assert_not_called()
                mock_print.reset_mock()

            # Testing invalid units.
            for unit in ["", "invalid", "inval1d_w1th_numb3rs"]:

                with self.assertRaises(SystemExit):
                    recipe.make_safe_recipe("name", ["123" + unit], ["salt"], chemical_library={"salt" : None}, recipe_library={})
                    mock_print.assert_called()
                    mock_print.reset_mock()

    def test_magnitude_validity(self):
        """Testing that the function checks that the magnitude of each concentration value is a positive number."""
        with mock.patch("buf.commands.recipe.print") as mock_print:

            # Testing valid quantities.
            for quantity in ["100", "100.1", "0.1", ".1", "10."]:
                recipe.make_safe_recipe("name", [quantity + "M"], ["salt"], recipe_library={}, chemical_library={"salt" : None})
                mock_print.assert_not_called()
                mock_print.reset_mock()

            # Testing invalid quantities.
            for quantity in ["", "-1", "0"]:
                with self.assertRaises(SystemExit):
                    recipe.make_safe_recipe("name", [quantity + "L"], ["salt"], chemical_library={"salt" : None}, recipe_library={})
                    mock_print.assert_called()
                    mock_print.reset_mock()

class TestRecipe(TestCase):
    """Tests the recipe.Recipe class."""

    def test_string_cast(self):
        """Tests the cast of a Recipe to a string."""
        with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value={"salt": None, "pepper" : None}):
            test_recipe = recipe.Recipe("name", ["300mM", "4L"], ["salt", "pepper"])
            self.assertEqual(str(test_recipe), "name 300mM salt 4L pepper")

    def equals_check(self):
        """Testing that two Recipes with identical names and contents are equal. Also checks the case when the
        contents of two Recipes are identical but are in different orders (e.g. Recipe A has contents of "2M salt 10%
        glycerol", while Recipe B has contents  "10% glycerol 2M salt". These two Recipes should be equal). """
        with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value={"salt": None, "pepper": None}):

            # Changing all possible variables (name, units, chemical name, concentration)
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

            # Testing that two recipes that have identical contents, but in different orders, are equal.
            forwards_recipe = recipe.Recipe("my_recipe", ["1M", "2M"], ["salt", "pepper"])
            backwards_recipe = recipe.Recipe("my_recipe", ["2M", "1M"], ["pepper", "salt"])

            self.assertEqual(forwards_recipe, backwards_recipe)


class TestAddRecipesFromFile(TestCase):
    """Tests recipe.add_recipe_from_file."""

    def test_invalid_file_name(self):
        """Tests that the function checks whether """
        with mock.patch("buf.commands.recipe.open") as mock_open:
            with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value = {"Arg" : None, "KCl" : None,  "salt" : None, "pepper" : None}):
                with mock.patch("buf.commands.recipe.load_recipes", return_value = {"wash" : None, "elution" : None}):
                    with mock.patch("buf.commands.recipe.print") as mock_print:
                        with mock.patch("buf.commands.recipe.os.path.isfile", return_value = False):

                            # Testing an invalid file name.
                            with self.assertRaises(SystemExit):
                                recipe.add_recipes_from_file("invalidfile")

    def test_invalid_file_contents(self):
        """Tests that the function raises SystemExit (i.e. cleanly exits the program opposed to crashing) \
            when the specified file has invalid contents (see recipe.instructions for more information on what \
            constitutes a valid file)."""

        with mock.patch("buf.commands.recipe.open") as mock_open:
            with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value = {"Arg" : None, "KCl" : None,  "salt" : None, "pepper" : None}):
                with mock.patch("buf.commands.recipe.load_recipes", return_value = {"wash" : None, "elution" : None}):
                    with mock.patch("buf.commands.recipe.print") as mock_print:
                        with mock.patch("buf.commands.recipe.os.path.isfile", return_value = True):

                            # Invalid file contents
                            for file_contents in ["refold 500mM unknownchemical 5g Arg", "wash 300mM salt", "name 300weirdunit pepper",
                                                  "refold 300mM salt\nrefold 4M pepper", "name 300mM"]:
                                with self.assertRaises(SystemExit):

                                    mock_open.return_value.__enter__.return_value = StringIO(file_contents)
                                    recipe.add_recipes_from_file("whatever")
                                    mock_print.assert_called()
                                    mock_open.return_value.__enter__.return_value.write.assert_not_called()

                                    mock_print.reset_mock()

                            # Valid file contents
                            for file_contents in ["refold 300mM Arg", "refold 4mL pepper 10% salt", "refold 3M salt\nother 4% pepper"]:
                                mock_open.return_value.__enter__.return_value = StringIO(file_contents)
                                recipe.add_recipes_from_file("whatever")



    def test_correct_writing(self):
        """Tests that the function correctly appends the newly created recipes to the library file."""
        with mock.patch("buf.commands.recipe.print") as mock_print:
            with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value = {"Arg" : None, "KCl" : None,
                                                                                            "salt" : None, "pepper" : None}):
                temp_library_file = NamedTemporaryFile(mode="a+")
                with open(temp_library_file.name, "a") as file:
                    file.write("wash 3M salt 10% pepper\nelution 4g Arg\n")

                temp_file_to_add = NamedTemporaryFile(mode = "a+")
                with open(temp_file_to_add.name, "a") as file:
                    file.write("refold 4% KCl 3M salt\nother 4M Arg 10.5L pepper")

                with mock.patch("buf.commands.recipe.recipe_library_file", temp_library_file.name):
                    recipe.add_recipes_from_file(temp_file_to_add.name)

                    with open(temp_library_file.name, "r") as file:
                        contents = file.read()

                    self.assertEqual(contents, "wash 3M salt 10% pepper\nelution 4g Arg\nrefold 4% KCl 3M salt\nother 4M Arg 10.5L pepper\n")
                    mock_print.assert_called()

class TestSaveRecipeLibrary(TestCase):
    """Tests recipe.save_recipe_library."""

    def test_read_write(self):
        """Tests that the loading, saving, and again loading the recipe library leaves it unchanged."""

        # No need to include Arg and glycerol in library since existing chemicals are only checked for if their concentration is in molar.
        with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value = {"salt" : None, "pepper" : None}):
            temp_file = NamedTemporaryFile("w+")

            file_contents = "wash 300mM salt 4M pepper\nelution 5g Arg 20% glycerol\n"
            with open(temp_file.name, "w") as file:
                file.write(file_contents)

            with mock.patch("buf.commands.recipe.recipe_library_file", temp_file.name):
                read_recipe_dict = recipe.load_recipes()

                recipe.save_recipe_library(read_recipe_dict)

                read_again = recipe.load_recipes()

                self.assertEqual(read_recipe_dict, read_again)

class TestDeleteRecipe(TestCase):
    """Tests recipe.delete_recipe."""

    def test_name_check(self):
        """Tests that the function checks that the specified recipe to delete exists in the library."""
        with mock.patch("buf.commands.recipe.load_recipes", return_value = {}):
            with mock.patch("buf.commands.recipe.print") as mock_print:
                with self.assertRaises(SystemExit):
                    recipe.delete_recipe("unknown_recipe")
                    mock_print.assert_called()

    def test_delete(self):
        """Tests the removal of the specified recipe from the library."""
        with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value={"salt": None, "pepper": None}):

            temp_file = NamedTemporaryFile("w+")

            test_buffer_a = recipe.Recipe("buffer_a", ["300mM", "10L"], ["salt", "pepper"])
            test_buffer_b = recipe.Recipe("buffer_b", ["4ug", ".5M"], ["solute", "salt"])

            initial_library = {"buffer_a" : test_buffer_a, "buffer_b" : test_buffer_b}

            after_delete = {"buffer_b": test_buffer_b}

            with mock.patch("buf.commands.recipe.recipe_library_file", temp_file.name):
                recipe.save_recipe_library(initial_library)

                recipe.delete_recipe("buffer_a", prompt_for_confirmation=False)

                self.assertEqual(after_delete, recipe.load_recipes())

class TestDisplayRecipeInformation(TestCase):
    """Tests recipe.display_recipe_information"""

    def test_name_check(self):
        """Tests that the function checks that the recipe to display exists."""
        with mock.patch("buf.commands.recipe.load_recipes", return_value = {}):
            with self.assertRaises(SystemExit):
                recipe.display_recipe_information("unknown_recipe")
