# File name: test_unit.py
# Author: Jordan Juravsky
# Date created: 03-08-2018

"""Tests the buf.unit module."""

from unittest import mock, TestCase
import unittest
from buf import unit

class TestSplitUnitQuantity(TestCase):
    """Tests unit.split_unit_quantity."""

    def test_correct_split(self):
        """Tests that the function properly parses a string containing a concentration into a magnitude and unit."""
        for quantity in ["100", "1.0", "2343.5", ".1", "10.", "0", "-5"]:
            for symbol in ["M", "L", "mM", ""]:
                test_string = str(quantity)+symbol
                returned_magnitude, returned_symbol = unit.split_unit_quantity(test_string)
                self.assertEqual(quantity, returned_magnitude)
                self.assertEqual(symbol, returned_symbol)

class TestUnitLadder(TestCase):
    """Tests the make.UnitLadder class."""

    def test_correct_assembly(self):
        """Tests that the class properly converts a dictionary mapping unit symbols to their coefficients into a \
        unit hierarchy."""
        test_ladder = unit.UnitLadder({"uL" : 1e-6, "µL" : 1e-6, "mL" : 1e-3, "L" : 1})

        test_a = unit.UnitInfo(["µL", "uL"], 1e-6)
        test_b = unit.UnitInfo(["mL"], 1e-3)
        test_c = unit.UnitInfo(["L"], 1)

        test_a.greater = test_b
        test_b.lesser = test_a

        test_b.greater = test_c
        test_c.lesser = test_b

        test_dict = {"uL" : test_a, "µL" : test_a, "mL" : test_b, "L" : test_c}

        self.assertEqual(test_dict, test_ladder.symbol_to_info)


    def test_scale_checking(self):
        """Tests that the ladder correctly checks whether it can scale a given unit up/down."""
        test_ladder = unit.UnitLadder({"uL": 1e-6, "µL": 1e-6, "mL": 1e-3, "L": 1})

        self.assertTrue(test_ladder.can_scale_up_unit("mL"))
        self.assertTrue(test_ladder.can_scale_down_unit("mL"))

        self.assertFalse(test_ladder.can_scale_up_unit("L"))
        self.assertTrue(test_ladder.can_scale_down_unit("L"))

        self.assertTrue(test_ladder.can_scale_up_unit("µL"))
        self.assertFalse(test_ladder.can_scale_down_unit("uL"))

    def test_correct_scale(self):
        """Tests that the ladder can properly scale units up and down the ladder."""
        test_ladder = unit.UnitLadder({"uL": 1e-6, "µL": 1e-6, "mL": 1e-3, "L": 1})

        # Intentional switching between µL and uL
        self.assertEqual(test_ladder.scale_up_unit("uL"), ("mL", 1e-6 / 1e-3))
        self.assertEqual(test_ladder.scale_up_unit("µL"), ("mL", 1e-6 / 1e-3))
        self.assertEqual(test_ladder.scale_down_unit("L"), ("mL", 1 / 1e-3 ))

        with mock.patch("buf.unit.print") as mock_print:
            with self.assertRaises(SystemExit):
                test_ladder.scale_down_unit("µL")
                mock_print.assert_called()

class TestConversionMethods(TestCase):
    """Tests the convinience functions unit.mass_unit_to_grams, unit.volume_unit_to_litres, and unit.concentration_unit_to_molar."""

    def test_conversions(self):
        """Tests that the methods properly access the scale factors of the correct UnitInfo classes in their respective UnitLadders."""
        ladders = [unit.mass_units, unit.volume_units, unit.concentration_units]
        funcs = [unit.mass_unit_to_grams, unit.volume_unit_to_litres, unit.concentration_unit_to_molar]

        for ladder, func, in zip(ladders, funcs):
            for symbol in ladder.symbol_to_info.keys():
                self.assertEqual(ladder.symbol_to_info[symbol].scale_factor, func(symbol))

class TestScaleAndRoundUnitQuantity(TestCase):
    """Tests unit.scale_and_round_physical_quantity."""

    def test_scaling(self):
        """Tests the function properly scaling the magnitude of a physical quantity so that the magnitude is in the range \
        [1, 1000)."""

        self.assertEqual(unit.scale_and_round_physical_quantity(0.1, "L"), "100.0mL")
        self.assertEqual(unit.scale_and_round_physical_quantity(10 * 1e-6, "M"), "10.0µM")
        self.assertEqual(unit.scale_and_round_physical_quantity(1000, "mg"), "1.0g")

        self.assertEqual(unit.scale_and_round_physical_quantity(1.0, "mg"), "1.0mg")

    # TODO: needs to be updated when settings are added / custom rounding.
    def test_rounding(self):
        """Tests that the function rounds the magnitude of a physical quantity to 2 decimal places."""

        self.assertEqual(unit.scale_and_round_physical_quantity(123.456, "L"), "123.46L")
        self.assertEqual(unit.scale_and_round_physical_quantity(0.123456, "L"), "123.46mL")
        self.assertEqual(unit.scale_and_round_physical_quantity(10089, "µL"), "10.09mL")

if __name__ == '__main__':
    unittest.main()