# File name: test_chemicals.py
# Author: Jordan Juravsky
# Date created: 28-07-2018

from unittest import mock, TestCase
import unittest
from io import StringIO

from buf.commands import chemical

class ChemicalTest(TestCase):
    # TODO: change test to mock sys.exit and assert called, instead of the try/except block.
    def test_molar_mass_check(self):
            with mock.patch("buf.commands.chemical.print") as mock_print:
                try:
                    chemical.Chemical("not a number", ["valid name"])
                    raise Exception("Should not get to this line")
                except:
                    mock_print.assert_called()
                    self.assertRaises(SystemExit)
                mock_print.reset_mock()


                for test_molar_mass in [100, 123.4]:
                    self.assertEqual(chemical.Chemical(test_molar_mass, ["valid name"]).molar_mass, test_molar_mass)
                    self.assertEqual(chemical.Chemical(str(test_molar_mass), ["valid name"]).molar_mass, test_molar_mass)

                mock_print.assert_not_called()


    def test_string_cast(self):
        test_chemical = chemical.Chemical(300, ["salt", "pepper"])
        self.assertTrue(str(test_chemical), "300 salt pepper")

    def test_equals(self):
        one_chemical = chemical.Chemical(123.4, ["name1", "name2"])
        other_chemical = chemical.Chemical(123.4, ["name1", "name2"])
        self.assertEqual(one_chemical, other_chemical)

class AddChemicalTest(TestCase):

    # Tests that method will not write
    def test_name_collision(self):
        test_chemical = chemical.Chemical(100, ["salt"])
        with mock.patch("buf.commands.chemical.load_chemicals", return_value = {"salt" : test_chemical}) as my_mock:
            with mock.patch("buf.commands.chemical.open") as mock_open:
                with mock.patch("buf.commands.chemical.print") as mock_print:
                    chemical.add_chemical(123, ["salt"])
                    mock_open.return_value.__enter__.write.assert_not_called()
                    mock_print.assert_called()

    def test_writing(self):
        test_mass = 100
        test_names = ["a", "b", "c"]
        with mock.patch("buf.commands.chemical.load_chemicals", return_value={}):
            with mock.patch("buf.commands.chemical.open") as mock_open:
                chemical.add_chemical(test_mass, test_names)
                mock_open.return_value.__enter__.return_value.write.assert_called_with(str(chemical.Chemical(test_mass, test_names)) + "\n")

class LoadChemicalTest(TestCase):

    def test_correct_read(self):
        one_chemical = chemical.Chemical(123.4, ["name1", "name2"])
        other_chemical = chemical.Chemical(567.8, ["name3", "name4"])
        chemical_dict = {"name1" : one_chemical, "name2" : one_chemical, "name3" : other_chemical, "name4" : other_chemical}
        with mock.patch("buf.commands.chemical.open") as mock_open:
            mock_open.return_value.__enter__.return_value = StringIO(str(one_chemical) + "\n" + str(other_chemical))
            returned_dict = chemical.load_chemicals()
            self.assertEqual(chemical_dict, returned_dict)