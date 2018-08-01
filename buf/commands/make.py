# File name: make.py
# Author: Jordan Juravsky
# Date created: 31-07-2018

from buf.commands.recipe import mass_units, volume_units, molarity_units, valid_units
from buf.commands import chemical, recipe


from sys import exit


def make():
    pass



class Step:
    def __init__(self, name, concentration, amount_to_add):
        self.name = name
        self.concentration = concentration
        self.amount_to_add = amount_to_add

class BufferInstructions:

    def __init__(self, buffer_volume, recipe_name):

        buffer_quantity, buffer_unit = recipe.split_concentration(buffer_volume)

        if buffer_unit not in volume_units:
            print(f"Invalid unit: '{buffer_unit}' is not a valid unit of volume")


        self.steps = []

        chemicals = chemical.load_chemicals()
        recipes = recipe.load_recipes()

        if recipe_name not in recipes:
            # TODO: prompt user to add it.
            print(f"Name not found: '{recipe_name}' not in recipe library")
            exit()

        recipe_object = recipes[recipe_name]

        for concentration, chemical_name in zip(recipe_object.concentrations, recipe_object.chemical_names):

            if chemical_name not in chemicals:
                print(f"Name not found: '{chemical_name}' not in chemical library.")
                exit()

            chemical_object = chemicals[chemical_name]

            quantity, unit = recipe.split_concentration(concentration)

            # TODO: do I need to check units/quantities again?
            quantity = float(quantity)

            if unit in molarity_units:
                amount_to_add = str(molarity_units[unit] * chemical_object.molar_mass * buffer_volume) + "g"
            elif unit in volume_units + mass_units:
                amount_to_add = concentration
            elif unit == "%":
                amount_to_add = str(buffer_volume * quantity / 100) +




