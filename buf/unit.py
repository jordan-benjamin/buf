# File name: unit.py
# Author: Jordan Juravsky
# Date created: 03-08-2018

"""Module for handling physical quantities. Converts, scales, and rounds measurements with units.
A note on terminology used in this module and in the larger program as a whole: given a physical quantity "10L",
"10" is the quantity's magnitude, while "L" is the quantity's unit/symbol. """

from sys import exit
from buf import error_messages

class UnitInfo:
    """Record that stores a list of equivalent unit symbols, their scale factor (the factor one needs to multiply by
    to reach a standard unit, for example the scale factor of mL relative to L is 1e-3), and pointers to the units that are immediately
    larger and smaller than it (for example, the UnitInfo describing mL might point to L and uL)."""
    def __init__(self, symbols, scale_factor):
        self.symbols = symbols
        self.scale_factor = scale_factor
        self.greater = None
        self.lesser = None

    def __lt__(self, other):
        return self.scale_factor < other.scale_factor

    # NOTE: not checking self.lesser since then the method becomes self-referencing
    def __eq__(self, other):
        return set(self.symbols) == set(other.symbols) and self.scale_factor == other.scale_factor \
            and self.greater == other.greater

class UnitLadder:
    """Stores a hierarchy of units of a certain type, such as units of volume. Allows one to easily scale/convert physical
    quantities between units in the ladder.

    Some notes on terminology in this class:
        - "Scaling up" a physical quantity means making quantity's unit larger (for example, going from mL to L). This means
         that the magnitude of the physical quantity gets SMALLER after scaling up. The reverse is true for scaling down."""
    def __init__(self, unit_dict):

        symbol_to_info = {}

        # Have to make this list instead of using symbol_to_info.values() after the next loop, since duplicates will appear multiple times.
        unit_info_list = []

        for symbol, scale_factor in unit_dict.items():
            found = False
            for unit_info in symbol_to_info.values():
                if unit_info.scale_factor == scale_factor:
                    unit_info.symbols.append(symbol)
                    symbol_to_info[symbol] = unit_info
                    found = True
                    break
            if not found:
                new_unit_info = UnitInfo([symbol], scale_factor)
                unit_info_list.append(new_unit_info)
                symbol_to_info[symbol] = new_unit_info


        unit_info_list.sort()

        for index in range(len(unit_info_list)-1):
            first_info = unit_info_list[index]
            second_info = unit_info_list[index+1]

            first_info.greater = second_info
            second_info.lesser = first_info

        self.unit_info_list = unit_info_list
        self.symbol_to_info = symbol_to_info
        self.symbols = list(unit_dict.keys())

    def __contains__(self, item):
        return item in self.symbol_to_info

    def get_symbols(self):
        return list(self.symbol_to_info.keys())

    def get_scale_factor(self, symbol):
        """Return the scale factor of a given unit."""
        return self.symbol_to_info[symbol].scale_factor

    def can_scale_up_unit(self, symbol):
        """Checks if a unit exists in the ladder that is greater than the symbol given (which determines whether the
        ladder can scale a physical quantity with the given unit to a larger unit)."""
        if symbol not in self.symbol_to_info:
            error_messages.unit_not_in_ladder(symbol)

        unit_info = self.symbol_to_info[symbol]

        if unit_info.greater:
            return True
        else:
            return False

    def can_scale_down_unit(self, symbol):
        """Checks if a unit exists in the ladder that is lesser than the symbol given (which determines whether the
        ladder can scale a physical quantity with the given unit to a smaller unit)."""
        if symbol not in self.symbol_to_info:
            error_messages.unit_not_in_ladder(symbol)

        unit_info = self.symbol_to_info[symbol]

        if unit_info.lesser:
            return True
        else:
            return False


    def scale_up_unit(self, symbol):
        """Given a unit, returns the next unit larger than it, as well as the factor one would have to multiply
        the magnitude of a physical quantity by to convert to the new unit."""
        if symbol not in self.symbol_to_info:
            error_messages.unit_not_in_ladder(symbol)

        unit_info = self.symbol_to_info[symbol]

        if unit_info.greater:
            return unit_info.greater.symbols[0], (unit_info.scale_factor / unit_info.greater.scale_factor)
        else:
            error_messages.no_greater_unit_in_ladder(symbol)


    def scale_down_unit(self, symbol):
        """Given a unit, returns the next unit smaller than it, as well as the factor one would have to multiply
        the magnitude of a physical quantity by to convert to the new unit."""
        if symbol not in self.symbol_to_info:
            error_messages.unit_not_in_ladder(symbol)

        unit_info = self.symbol_to_info[symbol]

        if unit_info.lesser:
            return unit_info.lesser.symbols[0], (unit_info.scale_factor / unit_info.lesser.scale_factor)
        else:
            error_messages.no_lesser_unit_in_ladder(symbol)


# NOTE: This method does NOT do any type checking.
def split_unit_quantity(string):
    """Given a physical quantity as a string, returns a tuple containing the quantity's magnitude and unit, both
    as strings."""
    quantity = ""
    index = 0
    quantity_characters = [str(num) for num in range(10)] + [".", "-", "+"]
    for character in string:
        if character in quantity_characters:
            quantity+= character
            index += 1
        else:
            break
    symbol = string[index:]
    return quantity, symbol

def scale_up_physical_quantity(quantity: float, symbol: str):
    """Scales up a physical quantity (ie. unit gets larger, magnitude gets smaller) until the magnitude is in the
    range [1, 1000) or there is no greater unit to scale to. For example, "10000mL" would be scaled up to "10L"."""
    if symbol in volume_units:
        ladder = volume_units
    elif symbol in mass_units:
        ladder = mass_units
    elif symbol in concentration_units:
        ladder = concentration_units
    else:
        error_messages.unit_not_in_any_ladder(symbol)


    while quantity >= 1000 and ladder.can_scale_up_unit(symbol):
        new_symbol, scale_factor = ladder.scale_up_unit(symbol)
        quantity *= scale_factor
        symbol = new_symbol

    return quantity, symbol


def scale_down_physical_quantity(magnitude: float, symbol: str):
    """Scales down a physical quantity (ie. unit gets smaller, magnitude gets larger) until the magnitude is in the
        range [1, 1000) or there is no lesser unit to scale to. For example, "0.1L" would be scaled down to "100mL"."""
    if symbol in volume_units:
        ladder = volume_units
    elif symbol in mass_units:
        ladder = mass_units
    elif symbol in concentration_units:
        ladder = concentration_units
    else:
        error_messages.unit_not_in_any_ladder(symbol)

    while magnitude < 1 and ladder.can_scale_down_unit(symbol):
        new_symbol, scale_factor = ladder.scale_down_unit(symbol)
        magnitude *= scale_factor
        symbol = new_symbol

    return magnitude, symbol

def scale_and_round_physical_quantity(magnitude: float, symbol : str):
    """Scales a physical quantity up/down so that its magnitude is in the range [1,1000), before rounding the magnitude
    and returning the magnitude combined with the unit as a string."""
    if magnitude >= 1000:
        magnitude, symbol = scale_up_physical_quantity(magnitude, symbol)
    elif magnitude < 1:
        magnitude, symbol = scale_down_physical_quantity(magnitude, symbol)

    magnitude = round(magnitude, 2)

    return str(magnitude) + symbol


# Standardised to litres.
volume_units = UnitLadder({"L" : 1, "mL" : 1e-3, "µL" : 1e-6, "uL": 1e-6})

# Standardised to grams.
mass_units = UnitLadder({"kg" : 1000, "g" : 1, "mg" : 1e-3, "µg": 1e-6, "ug" : 1e-6})

# Standardised to molar.
concentration_units = UnitLadder({"M" : 1, "mM" : 1e-3, "µM" : 1e-6, "uM" : 1e-6})

valid_units = volume_units.symbols + mass_units.symbols + concentration_units.symbols + ["%"]

def volume_unit_to_litres(symbol):
    """Convenience function that returns the factor one must multiply to convert a physical quantity with the specified
    unit of volume into litres."""
    return volume_units.get_scale_factor(symbol)

def concentration_unit_to_molar(symbol):
    """Convenience function that returns the factor one must multiply to convert a physical quantity with the specified
        unit of concentration into molar."""
    return concentration_units.get_scale_factor(symbol)

def mass_unit_to_grams(symbol):
    """Convenience function that returns the factor one must multiply to convert a physical quantity with the specified
        unit of mass into grams."""
    return mass_units.get_scale_factor(symbol)