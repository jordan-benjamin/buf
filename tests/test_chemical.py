# File name: test_chemical.py
# Author: Jordan Juravsky
# Date created: 28-07-2018

from unittest import mock, TestCase
from io import StringIO

from buf.commands import chemical

class MakeSafeChemicalTest(TestCase):


    def test_molar_mass_check(self):
        with mock.patch("buf.commands.chemical.print") as mock_print:
            for test_molar_mass in [0, -10, "not a number"]:
                try:
                    chemical.make_safe_chemical(test_molar_mass, ["valid name"], {})
                except:
                    pass

                self.assertRaises(SystemExit)
                mock_print.assert_called()

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
                chemical.add_chemical(test_mass, test_names)
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