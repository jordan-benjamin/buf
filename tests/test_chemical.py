# File name: test_chemical.py
# Author: Jordan Juravsky
# Date created: 28-07-2018

from unittest import mock, TestCase
from io import StringIO

from buf.commands import chemical

from tempfile import NamedTemporaryFile

class MakeSafeChemicalTest(TestCase):

    def test_molar_mass_check(self):
        with mock.patch("buf.commands.chemical.print") as mock_print:
            for test_molar_mass in [0, -10, "not a number"]:
                with self.assertRaises(SystemExit):
                    chemical.make_safe_chemical(test_molar_mass, ["valid name"], {})
                    mock_print.assert_called()
                    mock_print.reset_mock()

            mock_print.reset_mock()

            for test_molar_mass in [100, 123.4]:
                self.assertEqual(chemical.make_safe_chemical(test_molar_mass, ["valid name"]).molar_mass, test_molar_mass)
                self.assertEqual(chemical.make_safe_chemical(str(test_molar_mass), ["valid name"]).molar_mass, test_molar_mass)
                mock_print.assert_not_called()

    def test_name_collision(self):
        with mock.patch("buf.commands.chemical.print") as mock_print:
                # Ensuring an invalid chemical is not created
                try:
                    chemical.make_safe_chemical(123, ["salt", "pepper"], {"salt": None})
                except:
                    pass

                self.assertRaises(SystemExit)
                mock_print.assert_called()


                # Ensuring a valid chemical is created.
                chemical.make_safe_chemical(123, ["salt"], {})



class ChemicalTest(TestCase):
    def test_string_cast(self):
        test_chemical = chemical.Chemical(300, ["salt", "pepper"])
        self.assertTrue(str(test_chemical), "300 salt pepper")

    def test_equals(self):
        one_chemical = chemical.Chemical(123.4, ["name1", "name2"])
        other_chemical = chemical.Chemical(123.4, ["name1", "name2"])
        self.assertEqual(one_chemical, other_chemical)

class AddChemicalTest(TestCase):

    def test_writing(self):
        test_mass = 100
        test_names = ["a", "b", "c"]
        with mock.patch("buf.commands.chemical.load_chemicals", return_value={}):
            with mock.patch("buf.commands.chemical.open") as mock_open:
                chemical.add_single_chemical(test_mass, test_names)
                mock_open.return_value.__enter__.return_value.write.assert_called_with(str(chemical.make_safe_chemical(test_mass, test_names)) + "\n")

class LoadChemicalTest(TestCase):

    def test_correct_read(self):
        one_chemical = chemical.Chemical(123.4, ["name1", "name2"])
        other_chemical = chemical.Chemical(567.8, ["name3", "name4"])
        chemical_dict = {"name1" : one_chemical, "name2" : one_chemical, "name3" : other_chemical, "name4" : other_chemical}
        with mock.patch("buf.commands.chemical.open") as mock_open:
            mock_open.return_value.__enter__.return_value = StringIO(str(one_chemical) + "\n" + str(other_chemical))
            returned_dict = chemical.load_chemicals()
            self.assertEqual(chemical_dict, returned_dict)

class TestAddFromFile(TestCase):

    def test_errors(self):
        with mock.patch("buf.commands.chemical.open") as mock_open:
            with mock.patch("buf.commands.chemical.load_chemicals", return_value = {"Arg" : None, "KCl" : None}):
                with mock.patch("buf.commands.chemical.print") as mock_print:
                    # Invalid file contents
                    for file_contents in ["100 salt pepper\n200 salt", "NotANumber salt pepper", "123 KCl pepper", \
                                          "0 validname othervalidname\n100 salt pepper", "-2 salt"]:
                        with self.assertRaises(SystemExit):

                            mock_open.return_value.__enter__.return_value = StringIO(file_contents)
                            chemical.add_chemicals_from_file("whatever")
                            mock_print.assert_called()
                            mock_open.return_value.__enter__.return_value.write.assert_not_called()

                            mock_print.reset_mock()

                    # Valid file contents
                    for file_contents in ["100 salt pepper\n200 name\n123.5 has three names"]:
                        mock_open.return_value.__enter__.return_value = StringIO(file_contents)
                        chemical.add_chemicals_from_file("whatever")



    def test_correct_writing(self):
        temp_library_file = NamedTemporaryFile(mode="a+")
        with open(temp_library_file.name, "a") as file:
            file.write("100 salt pepper\n154.25 DTT\n")

        temp_file_to_add = NamedTemporaryFile(mode = "a+")
        with open(temp_file_to_add.name, "a") as file:
            file.write("74.55 KCl\n68.08 imidazole imi")

        with mock.patch("buf.commands.chemical.chemical_library_file", temp_library_file.name):
            with mock.patch("buf.commands.chemical.print") as mock_print:
                chemical.add_chemicals_from_file(temp_file_to_add.name)
                mock_print.assert_called()

            with open(temp_library_file.name, "r") as file:
                contents = file.read()

            self.assertEqual(contents, "100 salt pepper\n154.25 DTT\n74.55 KCl\n68.08 imidazole imi\n")


class SaveChemicalLibraryTest(TestCase):
    def test_read_write(self):
        temp_file = NamedTemporaryFile("w+")

        file_contents = "100.0 salt pepper\n0.5 Arg Arginine\n54.55 NaCl\n"
        with open(temp_file.name, "w") as file:
            file.write(file_contents)

        with mock.patch("buf.commands.chemical.chemical_library_file", temp_file.name):
            read_chemical_dict = chemical.load_chemicals()

            chemical.save_chemical_library(read_chemical_dict)

            read_again = chemical.load_chemicals()

            self.assertEqual(read_chemical_dict, read_again)

class NickNameTest(TestCase):

    def test_errors(self):
        with mock.patch("buf.commands.chemical.load_chemicals", return_value = {"NaCl" : None, "Arg" : None}):
            with mock.patch("buf.commands.chemical.print") as mock_print:
                for existing_name, new_name in [("unknown", "nickname"), ("NaCl", "Arg"), ("NaCl", "NaCl")]:
                    with self.assertRaises(SystemExit):
                        chemical.nickname_chemical(existing_name, new_name)
                        mock_print.assert_called()
                    mock_print.reset_mock()

    def test_correct_write(self):
        temp_file = NamedTemporaryFile("w+")

        file_contents = "100.0 salt pepper\n0.5 Arg Arginine\n54.55 NaCl\n"
        with open(temp_file.name, "w") as file:
            file.write(file_contents)

        with mock.patch("buf.commands.chemical.chemical_library_file", temp_file.name):
            read_chemical_dict = chemical.load_chemicals()

            chemical_object = read_chemical_dict["salt"]

            chemical_object.names.append("newname")

            read_chemical_dict["newname"] = chemical_object

            chemical.nickname_chemical("salt", "newname")

            new_dict = chemical.load_chemicals()

            self.assertEqual(read_chemical_dict, new_dict)

class TestDeleteChemical(TestCase):

    def test_errors(self):

        with mock.patch("buf.commands.chemical.load_chemicals", return_value = {"salt" : None, "pepper" : None}):
            with mock.patch("buf.commands.chemical.print") as mock_print:
                with self.assertRaises(SystemExit):
                    chemical.delete_chemical("unknown_chemical")
                    mock_print.assert_called()

    def test_complete_delete(self):

        temp_file = NamedTemporaryFile("w+")

        test_salt_and_pepper = chemical.Chemical(200, ["salt", "pepper"])
        test_kcl = chemical.Chemical(123.4, ["KCl"])

        initial_library = {"salt" : test_salt_and_pepper, "pepper" : test_salt_and_pepper, "KCl" : test_kcl}

        after_delete = {"KCl": test_kcl}

        with mock.patch("buf.commands.chemical.chemical_library_file", temp_file.name):
            chemical.save_chemical_library(initial_library)

            chemical.delete_chemical("salt", complete_deletion=True, prompt_for_confirmation=False)

            self.assertEqual(after_delete, chemical.load_chemicals())

    def test_incomplete_delete(self):

        temp_file = NamedTemporaryFile("w+")

        test_salt_and_pepper = chemical.Chemical(200, ["salt", "pepper"])
        test_kcl = chemical.Chemical(123.4, ["KCl"])

        test_pepper = chemical.Chemical(200, ["pepper"])

        initial_library = {"salt" : test_salt_and_pepper, "pepper" : test_salt_and_pepper, "KCl" : test_kcl}

        after_delete = {"KCl": test_kcl, "pepper" : test_pepper}

        with mock.patch("buf.commands.chemical.chemical_library_file", temp_file.name):
            chemical.save_chemical_library(initial_library)

            chemical.delete_chemical("salt", complete_deletion=False, prompt_for_confirmation=False)

            self.assertEqual(after_delete, chemical.load_chemicals())

