# File name: make.py
# Author: Jordan Juravsky
# Date created: 31-07-2018

from buf.commands import chemical, recipe
from buf import unit, error_messages
import tabulate

instructions = """buf make:

This subcommand calculates the amount of each chemical that is required \
to make a solution/buffer of a given volume.

To make a solution using a previously defined recipe (see 'buf help recipe' for more information), \
use 'buf make <volume> <recipe_name>'. For example, to make 2L of a buffer named 'wash', \
(where 'wash' has already been defined with 'buf recipe -a'), use 'buf make 2L wash'. 

Alternatively, one can define a solution on the spot, with 'buf make <volume> (<concentration> \
<chemical_name>)...'. For example, 'buf make 0.5L 300mM NaCl 10% glycerol'. \
Note that in this case, the molar mass of NaCl must already be stored in your chemical library. 

* Note: if one wishes to copy and paste the table outputted by 'buf make' (for example, into a text file to print), \
make sure that one uses the font 'New Courier', in order for the table to be formatted properly. 
"""

def make(options: dict):
    if options["<recipe_name>"]:
        recipe_object = get_recipe(options["<recipe_name>"])
    else:
        recipe_object = recipe.make_safe_recipe("temp", options["<concentrations>"], options["<chemical_names>"], recipe_library= {})

    buffer_volume_in_litres = get_buffer_litres(options["<volume>"])

    buffer = BufferInstructions(buffer_volume_in_litres, recipe_object)
    buffer.print()


def get_buffer_litres(volume_as_string: str):
    magnitude, symbol = unit.split_unit_quantity(volume_as_string)

    try:
        magnitude = float(magnitude)
    except:
        error_messages.non_number_buffer_volume_magnitude(magnitude)

    if magnitude <= 0:
        error_messages.non_positive_buffer_volume_magnitude(magnitude)

    if symbol not in unit.volume_units:
        error_messages.invalid_buffer_volume_unit(symbol)

    return magnitude * unit.volume_unit_to_litres(symbol)


def calculate_amount_to_add(buffer_volume_in_litres: float, concentration: str, chemical_name: str, chemical_library: dict):
    magnitude, symbol = unit.split_unit_quantity(concentration)

    if symbol in unit.concentration_units:
        chemical_object = chemical_library[chemical_name]

    magnitude = float(magnitude)

    if symbol in unit.volume_units or symbol in unit.mass_units:
        pass # If a constant volume or mass is specified, the amount does not change depending on the buffer volume.
    elif symbol in unit.concentration_units:
        magnitude = magnitude * unit.concentration_unit_to_molar(symbol) * chemical_object.molar_mass * buffer_volume_in_litres
        symbol = "g"
    elif symbol == "%":
        magnitude = magnitude / 100 * buffer_volume_in_litres
        symbol = "L"

    return unit.scale_and_round_unit_quantity(magnitude, symbol)

def get_recipe(recipe_name: str):
    recipe_library = recipe.load_recipes()

    if recipe_name not in recipe_library:
        error_messages.recipe_not_found(recipe_name)

    return recipe_library[recipe_name]


class Step:
    def __init__(self, name: str, concentration: str, amount_to_add: str):
        self.name = name
        self.concentration = concentration
        self.amount_to_add = amount_to_add
    def __eq__(self, other):
        return self.name == other.name and self.concentration == other.concentration and self.amount_to_add == other.amount_to_add

class BufferInstructions:

    def __init__(self, buffer_volume_in_litres: float, recipe_object: recipe.Recipe):

        self.steps = []

        chemical_library = chemical.load_chemicals()

        for concentration, chemical_name in zip(recipe_object.concentrations, recipe_object.chemical_names):
            self.steps.append(Step(chemical_name, concentration,
                                   calculate_amount_to_add(buffer_volume_in_litres, concentration, chemical_name, chemical_library)))

    def print(self):
        matrix = [[step.name, step.concentration, step.amount_to_add] for step in self.steps]

        print(tabulate.tabulate(matrix, headers=["Chemical Name", "Concentration", "Amount to Add"], tablefmt="fancy_grid"))
