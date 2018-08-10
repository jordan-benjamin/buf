# File name: test_make.py
# Author: Jordan Juravsky
# Date created: 08-08-2018

from unittest import mock, TestCase
from buf.commands import make, recipe, chemical
from buf import unit

class GetBufferLitresTest(TestCase):

    def test_errors(self):
        with mock.patch("buf.commands.make.print") as mock_print:
            for invalid_volume in ["10", "0L", "L", "45g", "-12L"]:
                with self.assertRaises(SystemExit):
                    make.get_buffer_litres(invalid_volume)
                    mock_print.assert_called()
                    mock_print.reset_mock()

    def test_conversion(self):
        for volume, volume_in_litres in zip(["10L", "10.5L", "0.1L", "20mL", "50µL", "50uL"], [10, 10.5, 0.1, 0.02, 50 * 1e-6, 50 * 1e-6]):
            converted_volume = make.get_buffer_litres(volume)
            self.assertEqual(volume_in_litres, converted_volume)

class CalculateAmountToAddTest(TestCase):

    def test_volume_and_mass_units(self):

        inputs = [float(i) for i in range(1,100)]

        for buffer_volume in range(1,10):
            for symbol in ["ug", "µg", "mg", "g", "µL", "uL", "mL", "L"]:
                for input in inputs:
                    self.assertEqual(unit.scale_and_round_unit_quantity(input, symbol),
                                     make.calculate_amount_to_add(buffer_volume, str(input)+symbol, "chemical_name", {}))

    def test_percent_volume(self):

        inputs = [i for i in range(1,100)]

        for buffer_volume in range(1,10):
            for input in inputs:
                self.assertEqual(unit.scale_and_round_unit_quantity(input*buffer_volume/100, "L"),
                                 make.calculate_amount_to_add(buffer_volume, str(input)+"%", "chemical_name", {}))

    def test_molarity_units(self):

        inputs = [i for i in range(1,100)]

        nacl = chemical.Chemical(58.44, ["NaCl"])

        chemical_library = {"NaCl" : nacl}

        for buffer_volume in range(1,10):
            for input in inputs:
                self.assertEqual(unit.scale_and_round_unit_quantity(58.44 * buffer_volume * input, "g"),
                                 make.calculate_amount_to_add(buffer_volume, str(input)+"M", "NaCl", chemical_library))


class BufferInstructionsTest(TestCase):

    def test_step_making(self):
        nacl = chemical.Chemical(58.44, ["NaCl"])
        kcl = chemical.Chemical(74.55, ["KCl"])

        test_recipe = recipe.Recipe("my_recipe", ["300mM", "4g"], ["NaCl", "KCl"])

        with mock.patch("buf.commands.make.chemical.load_chemicals", return_value = {"NaCl" : nacl, "KCl" : kcl}):
            test_buffer_instructions = make.BufferInstructions(2, test_recipe)

            correct_steps = [make.Step("NaCl", "300mM", unit.scale_and_round_unit_quantity(58.44 * 0.3 * 2, "g")),
                             make.Step("KCl", "4g", "4.0g")]

            self.assertEqual(test_buffer_instructions.steps, correct_steps)

class GetRecipeTest(TestCase):

    def test_errors(self):
        with mock.patch("buf.commands.make.recipe.load_recipes", return_value = {"my_recipe" : None}):

            # Testing an invalid recipe name.
            with self.assertRaises(SystemExit):
                should_crash = make.get_recipe("not_in_library")

            # Testing a valid recipe name.
            shouldnt_crash = make.get_recipe("my_recipe")