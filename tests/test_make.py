# File name: test_make.py
# Author: Jordan Juravsky
# Date created: 08-08-2018

"""Tests the buf.commands.make module."""

from unittest import mock, TestCase
from buf.commands import make, recipe, chemical
from buf import unit

class TestGetBufferLitres(TestCase):
    """Tests make.get_buffer_litres."""

    def test_invalid_inputs(self):
        """Tests that the function properly handles (i.e. raise SystemExit) for inputs that have either non-positive \
        magnitudes or a unit that is not one of volume."""
        with mock.patch("buf.commands.make.print") as mock_print:
            for invalid_volume in ["10", "0L", "L", "45g", "-12L"]:
                with self.assertRaises(SystemExit):
                    make.get_buffer_litres(invalid_volume)
                    mock_print.assert_called()
                    mock_print.reset_mock()

    def test_conversion(self):
        """Tests that the function properly converts the input to a value in litres."""
        for volume, volume_in_litres in zip(["10L", "10.5L", "0.1L", "20mL", "50µL", "50uL"], [10, 10.5, 0.1, 0.02, 50 * 1e-6, 50 * 1e-6]):
            converted_volume = make.get_buffer_litres(volume)
            self.assertEqual(volume_in_litres, converted_volume)


class TestCalculateAmountToAdd(TestCase):
    """Tests make.calculate_amount_to_add."""

    def test_volume_and_mass_units(self):
        """Tests that when a physical quantity of mass or volume is passed into the function, it returns that same amount, \
        scaled and rounded properly."""

        inputs = [float(i) for i in range(1,100)]

        for buffer_volume in range(1,10):
            for symbol in ["ug", "µg", "mg", "g", "µL", "uL", "mL", "L"]:
                for input in inputs:
                    self.assertEqual(unit.scale_and_round_physical_quantity(input, symbol),
                                     make.calculate_amount_to_add(buffer_volume, str(input)+symbol, "chemical_name", {}))

    def test_percent_volume(self):
        """Tests that when a percent volume is passed into the function, that fraction of the total buffer volume is returned, \
        scaled and rounded properly."""

        inputs = [i for i in range(1,100)]

        for buffer_volume in range(1,10):
            for input in inputs:
                self.assertEqual(unit.scale_and_round_physical_quantity(input * buffer_volume / 100, "L"),
                                 make.calculate_amount_to_add(buffer_volume, str(input)+"%", "chemical_name", {}))

    def test_molarity_units(self):
        """Tests that when a concentration in molar is passed into the function, it returns the chemicals molar mass \
        * concentration in molar * buffer volume in litres, scaled and rounded properly."""

        inputs = [i for i in range(1,100)]

        nacl = chemical.Chemical(58.44, ["NaCl"])

        chemical_library = {"NaCl" : nacl}

        for buffer_volume in range(1,10):
            for input in inputs:
                self.assertEqual(unit.scale_and_round_physical_quantity(58.44 * buffer_volume * input, "g"),
                                 make.calculate_amount_to_add(buffer_volume, str(input)+"M", "NaCl", chemical_library))


class TestBufferInstructions(TestCase):
    """Tests the make.BufferInstructions class."""

    def test_step_making(self):
        """Test that the class properly converts a Recipe into a series of Steps."""
        nacl = chemical.Chemical(58.44, ["NaCl"])
        kcl = chemical.Chemical(74.55, ["KCl"])

        test_recipe = recipe.Recipe("my_recipe", ["300mM", "4g"], ["NaCl", "KCl"])

        with mock.patch("buf.commands.make.chemical.load_chemicals", return_value = {"NaCl" : nacl, "KCl" : kcl}):
            test_buffer_instructions = make.BufferInstructions(2, test_recipe)

            correct_steps = [make.Step("NaCl", "300mM", unit.scale_and_round_physical_quantity(58.44 * 0.3 * 2, "g")),
                             make.Step("KCl", "4g", "4.0g")]

            self.assertEqual(test_buffer_instructions.steps, correct_steps)

class TestGetRecipe(TestCase):
    """Tests make.get_recipe."""

    def test_name_check(self):
        """Tests that the function checks that the specified recipe exists in the library."""
        with mock.patch("buf.commands.make.recipe.load_recipes", return_value = {"my_recipe" : None}):

            # Testing an invalid recipe name.
            with self.assertRaises(SystemExit):
                should_crash = make.get_recipe("not_in_library")

            # Testing a valid recipe name.
            shouldnt_crash = make.get_recipe("my_recipe")