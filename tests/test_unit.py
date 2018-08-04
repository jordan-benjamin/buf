# File name: test_unit.py
# Author: Jordan Juravsky
# Date created: 03-08-2018

from unittest import mock, TestCase

from buf import unit

class SplitUnitQuantityTest(TestCase):

    def test_correct_split(self):
        for quantity in ["100", "1.0", "2343.5", ".1", "10."]:
            for symbol in ["M", "L", "mM", ""]:
                test_string = str(quantity)+symbol
                returned_quantity, returned_unit = unit.split_unit_quantity(test_string)
                self.assertEqual(quantity, returned_quantity)
                self.assertEqual(symbol, returned_unit)

class UnitLadderTest(TestCase):

    def test_correct_assembly(self):
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


    def test_correct_scale(self):
        test_ladder = unit.UnitLadder({"uL": 1e-6, "µL": 1e-6, "mL": 1e-3, "L": 1})

        # Intentional switching between µL and uL
        self.assertEqual(test_ladder.scale_up("uL"), ("mL", 1e-3 / 1e-6))
        self.assertEqual(test_ladder.scale_up("µL"), ("mL", 1e-3 / 1e-6))
        self.assertEqual(test_ladder.scale_down("L"), ("mL",  1e-3 / 1))

        self.assertTrue(test_ladder.can_scale_up("mL"))
        self.assertTrue(test_ladder.can_scale_down("mL"))

        self.assertFalse(test_ladder.can_scale_up("L"))
        self.assertTrue(test_ladder.can_scale_down("L"))

        self.assertTrue(test_ladder.can_scale_up("µL"))
        self.assertFalse(test_ladder.can_scale_down("uL"))

        with mock.patch("buf.unit.print") as mock_print:
            try:
                test_ladder.scale_down("µL")
            except:
                pass
            self.assertRaises(SystemExit)
            mock_print.assert_called()