# File name: test_recipe.py
# Author: Jordan Juravsky
# Date created: 31-07-2018

from unittest import mock, TestCase

from tempfile import NamedTemporaryFile

from io import StringIO


from buf.commands import recipe


class MakeRecipeTest(TestCase):

    def test_spaces_in_name(self):
        with mock.patch("buf.commands.recipe.load_recipes", return_value = {}):
            with self.assertRaises(SystemExit):
                should_crash = recipe.make_safe_recipe("contains spaces", ["10%"], ["glycerol"])

            shouldnt_crash = recipe.make_safe_recipe("doesnt_contain_spaces", ["10%"], ["glycerol"])

    def test_existing_chemical_check(self):

            with mock.patch("buf.commands.recipe.print") as mock_print:
                # Testing the code stops if no matching chemical
                with self.assertRaises(SystemExit):
                    recipe.make_safe_recipe("boop", ["300mM"], ["Salt"], chemical_library= {}, recipe_library={})
                    mock_print.assert_called()

                mock_print.reset_mock()

                # Testing code words if chemical exists. Also verifies that a chemical is only checked to exist in the chemical
                # library if concentration is specified in molar (i.e. glycerol not in library, should not be checked since concentration
                # is in % volume).
                recipe.make_safe_recipe("boop", ["300mM", "10%"], ["salt", "glycerol"], chemical_library={"salt" : None}, recipe_library= {})
                mock_print.assert_not_called()


    def test_unit_validity(self):
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

    def test_quantity_validity(self):
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

    def test_string_cast(self):
        with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value={"salt": None, "pepper" : None}):
            test_recipe = recipe.Recipe("name", ["300mM", "4L"], ["salt", "pepper"])
            self.assertEqual(str(test_recipe), "name 300mM salt 4L pepper")

    def equals_check(self):
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


class IntegratedTests(TestCase):

    def test_read_write(self):
        with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value={"salt": None, "pepper": None}):

            tmp_file = NamedTemporaryFile()
            with mock.patch("buf.commands.recipe.recipe_library_file", tmp_file.name):

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

class TestAddFromFile(TestCase):

    def test_errors(self):
        with mock.patch("buf.commands.recipe.open") as mock_open:
            with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value = {"Arg" : None, "KCl" : None,  "salt" : None, "pepper" : None}):
                with mock.patch("buf.commands.recipe.load_recipes", return_value = {"wash" : None, "elution" : None}):
                    with mock.patch("buf.commands.recipe.print") as mock_print:

                        # Testing an invalid file name.
                        with self.assertRaises(SystemExit):
                            recipe.add_recipes_from_file("invalidfile")

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

class SaveRecipeLibraryTest(TestCase):

    def test_read_write(self):
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

    def test_errors(self):

        with mock.patch("buf.commands.recipe.chemical.load_chemicals", return_value = {"salt" : None, "pepper" : None}):
            with mock.patch("buf.commands.recipe.print") as mock_print:
                with self.assertRaises(SystemExit):
                    recipe.delete_recipe("unknown_recipe")
                    mock_print.assert_called()

    def test_delete(self):
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

class DisplayRecipeInformationTest(TestCase):

    def test_errors(self):
        with mock.patch("buf.commands.recipe.load_recipes", return_value = {}):
            with self.assertRaises(SystemExit):
                recipe.display_recipe_information("unknown_recipe")
