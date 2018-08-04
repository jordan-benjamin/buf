# File name: unit.py
# Author: Jordan Juravsky
# Date created: 03-08-2018

from sys import exit

# TODO: add non-metric units?

class UnitInfo:
    def __init__(self, symbols, scale_factor):
        self.symbols = symbols
        self.scale_factor = scale_factor
        self.greater = None
        self.lesser = None

    def __lt__(self, other):
        return self.scale_factor < other.scale_factor

    def __str__(self):
        return f"({self.symbols}, {self.scale_factor}, {self.greater.symbols if self.greater else None})"

    # NOTE: not checking self.lesser since then the method becomes self-referencing
    def __eq__(self, other):
        return set(self.symbols) == set(other.symbols) and self.scale_factor == other.scale_factor \
            and self.greater == other.greater

class UnitLadder:
    def __init__(self, unit_dict):

        symbol_to_info = {}

        # Have to make this list instead of using symbol_to_info.values(), since duplicates will appear multiple times.
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

        # TODO: is the list necessary (i.e. delete?)
        self.unit_info_list = unit_info_list
        self.symbol_to_info = symbol_to_info
        self.symbols = list(unit_dict.keys())

    def __contains__(self, item):
        return item in self.symbol_to_info

    def get_scale_factor(self, symbol):
        return self.symbol_to_info[symbol].scale_factor

    def can_scale_up_unit(self, symbol):
        if symbol not in self.symbol_to_info:
            print(f"Unit symbol not found: '{symbol}' is not in unit ladder.")
            exit()

        unit_info = self.symbol_to_info[symbol]

        if unit_info.greater:
            return True
        else:
            return False

    def can_scale_down_unit(self, symbol):
        if symbol not in self.symbol_to_info:
            print(f"Unit symbol not found: '{symbol}' is not in unit ladder.")
            exit()

        unit_info = self.symbol_to_info[symbol]

        if unit_info.lesser:
            return True
        else:
            return False


    def scale_up_unit(self, symbol):
        if symbol not in self.symbol_to_info:
            print(f"Unit symbol not found: '{symbol}' is not in unit ladder.")
            exit()

        unit_info = self.symbol_to_info[symbol]

        if unit_info.greater:
            # Note: its current factor / new factor since the quantities are L / symbol, therefore
            # if you have unit x and want to go to y, you multiply by L / x , then divide by L / y.
            return unit_info.greater.symbols[0], (unit_info.scale_factor / unit_info.greater.scale_factor)
        else:
            print(f"No greater unit: '{symbol}' does not have a unit greater than it in the ladder.")
            exit()


    def scale_down_unit(self, symbol):
        if symbol not in self.symbol_to_info:
            print(f"Unit symbol not found: '{symbol}' is not in unit ladder.")
            exit()

        unit_info = self.symbol_to_info[symbol]

        if unit_info.lesser:
            return unit_info.lesser.symbols[0], (unit_info.scale_factor / unit_info.lesser.scale_factor)
        else:
            print(f"No lesser unit: '{symbol}' does not have a unit lesser than it in the ladder.")
            exit()


# NOTE: This method does NOT do any type checking.
def split_unit_quantity(string):
    # TODO: look into settings to find default unit if not specified.
    # TODO: handle bad inputs (no quantity or only ".")
    # TODO: check for valid unit (have list of acceptable units)
    quantity = ""
    index = 0
    quantity_characters = [str(num) for num in range(10)] + ["."]
    for character in string:
        if character in quantity_characters:
            quantity+= character
            index += 1
        else:
            break
    symbol = string[index:]
    return quantity, symbol

def scale_up_unit_quantity(quantity: float, symbol: str):
    # TODO: turn this into a single line with filter and list comprehension?
    if symbol in volume_units:
        ladder = volume_units
    elif symbol in mass_units:
        ladder = mass_units
    elif symbol in concentration_units:
        ladder = concentration_units
    else:
        print(f"Invalid unit: '{symbol}' is not in any symbol ladder")
        exit()


    while quantity >= 1000 and ladder.can_scale_up_unit(symbol):
        new_symbol, scale_factor = ladder.scale_up_unit(symbol)
        quantity *= scale_factor
        symbol = new_symbol

    return quantity, symbol


def scale_down_unit_quantity(quantity: float, symbol: str):
    # TODO: turn this into a single line with filter and list comprehension?
    if symbol in volume_units:
        ladder = volume_units
    elif symbol in mass_units:
        ladder = mass_units
    elif symbol in concentration_units:
        ladder = concentration_units
    else:
        print(f"Invalid unit: '{symbol}' is not in any symbol ladder")
        exit()

    while quantity < 1 and ladder.can_scale_down_unit(symbol):
        new_symbol, scale_factor = ladder.scale_down_unit(symbol)
        quantity *= scale_factor
        symbol = new_symbol

    return quantity, symbol

# TODO: check settings for number of decimal places to round.
def scale_and_round_unit_quantity(quantity: float, symbol : str):
    if quantity >= 1000:
        quantity, symbol = scale_up_unit_quantity(quantity, symbol)
    elif quantity < 1:
        quantity, symbol = scale_down_unit_quantity(quantity, symbol)

    quantity = round(quantity, 2)

    return str(quantity) + symbol

# TODO: add moles?
# TODO: add mg/ml and that stuff.
# Standardised to litres.
volume_units = UnitLadder({"L" : 1, "mL" : 1e-3, "µL" : 1e-6, "uL": 1e-6})

# Standardised to grams.
mass_units = UnitLadder({"kg" : 1000, "g" : 1, "mg" : 1e-3, "µg": 1e-6, "ug" : 1e-6})

# Standardised to molar.
concentration_units = UnitLadder({"M" : 1, "mM" : 1e-3, "µM" : 1e-6, "uM" : 1e-6})

valid_units = volume_units.symbols + mass_units.symbols + concentration_units.symbols + ["%"]

def volume_unit_to_litres(symbol):
    return volume_units.get_scale_factor(symbol)

def concentration_unit_to_molar(symbol):
    return concentration_units.get_scale_factor(symbol)

def mass_unit_to_grams(symbol):
    return mass_units.get_scale_factor(symbol)