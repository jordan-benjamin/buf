# File name: make.py
# Author: Jordan Juravsky
# Date created: 31-07-2018


from buf.commands import chemical, recipe

import tabulate

from sys import exit


def make(options):
    if options["<recipe_name>"]:
        recipe_object = get_recipe(options["<recipe_name>"])
    else:
        recipe_object = recipe.make_safe_recipe("", options["<concentration>"], options["<chemical_name>"], recipe_library= {})

    buffer_volume_in_litres = get_buffer_litres(options["<volume>"])

    buffer = BufferInstructions(buffer_volume_in_litres, recipe_object)
    buffer.print()


def get_buffer_litres(volume_as_string):
    quantity, unit = recipe.split_concentration(volume_as_string)

    try:
        quantity = float(quantity)
    except:
        print(f"Invalid quantity: '{quantity}' is not a valid number.")
        exit()

    if unit not in recipe.volume_units:
        print(f"Invalid unit: '{unit}' is not a valid unit of volume.")
        exit()

    return quantity * recipe.volume_units_to_litres[unit]


def calculate_amount_to_add(buffer_volume_in_litres, chemical_object, concentration):
    quantity, unit = recipe.split_concentration(concentration)

    # Try/catch this?
    quantity = float(quantity)

    # TODO: make sure unit is valid?

    if unit in recipe.volume_units or unit in recipe.mass_units:
        return concentration
    elif unit in recipe.concentration_units:
        # TODO: convert to mg if number is small.
        return str(quantity * recipe.concentration_units_to_molar[unit] * chemical_object.molar_mass * buffer_volume_in_litres) + "g"
    elif unit == "%":
        # TODO: accomodate non-litre volume units.
        return str(quantity / 100 * buffer_volume_in_litres) + "L"

def get_recipe(recipe_name):
    recipe_library = recipe.load_recipes()

    if recipe_name not in recipe_library:
        # TODO: prompt user to add it.
        # TODO: make a module to handle errors like these.
        print(f"Invalid recipe name: '{recipe_name}' not found in recipe library")
        exit()

    return recipe_library[recipe_name]


class Step:
    def __init__(self, name, concentration, amount_to_add):
        self.name = name
        self.concentration = concentration
        self.amount_to_add = amount_to_add

class BufferInstructions:

    def __init__(self, buffer_volume_in_litres, recipe_object):

        self.steps = []

        chemical_library = chemical.load_chemicals()

        for concentration, chemical_name in zip(recipe_object.concentrations, recipe_object.chemical_names):
            chemical_object = chemical_library[chemical_name]
            self.steps.append(Step(chemical_name, concentration, calculate_amount_to_add(buffer_volume_in_litres, chemical_object, concentration)))

        # TODO: sort the steps in some way (need to implement in Step class first).

    def print(self):
        matrix = [[step.name, step.concentration, step.amount_to_add] for step in self.steps]

        # TODO: what looks better: fancy_grid or the default?
        print(tabulate.tabulate(matrix, headers=["Chemical Name", "Concentration", "Amount to Add"], tablefmt="fancy_grid"))


