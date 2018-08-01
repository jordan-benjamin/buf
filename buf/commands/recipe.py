# File name: recipe.py
# Author: Jordan Juravsky
# Date created: 31-07-2018

if __name__ == '__main__':
    import chemical
else:
    from buf.commands import chemical

from sys import exit

import os
recipe_library_file = os.path.join(os.path.dirname(__file__), "../library/recipes.txt")

# TODO: is using u as a substitute for µ ok?
volume_units = {"L" : 1, "mL" : 1e-3, "µL" : 1e-6, "uL": 1e-6}
mass_units = { "kg" : 1000, "g" : 1, "mg" : 1e-3, "ug": 1e-6, "µg" : 1e-6}
molarity_units = {"M" : 1, "mM" : 1e-3, "uM" : 1e-6, "µM" : 1e-6}

# Casting a dictionary to a list returns a list of its keys.
valid_units = list(volume_units) + list(molarity_units) + list(mass_units) + ["%"]

def recipe():
    pass

class Recipe:
    # TODO: ensure that docopt with guarantee that the lengths of concentrations and chemical_names are the same.
    def __init__(self, name, concentrations, chemical_names):
        chemical_dict = chemical.load_chemicals()

        for concentration, chemical_name in zip(concentrations, chemical_names):
            if chemical_name not in chemical_dict:
                # TODO: prompt user to add chemical.
                print(f"Name not found: '{chemical_name}' not in chemical library.")
                exit()

            quantity, unit = split_concentration(concentration)

            # TODO: accept blank unit, load from settings.
            if unit not in valid_units:
                # TODO: display all valid units?
                print(f"Invalid unit: '{unit}' is not a valid unit.")
                exit()

            try:
                float_quantity = float(quantity)
            except:
                # TODO: change this message to mention numbers?
                print(f"Invalid quantity: '{quantity}' is not a valid quantity")
                exit()

        # TODO: any type checking for recipe name? Check if recipe already exists (do that first).
        # TODO: check if name is blank? will docopt let that happen?
        self.name = name
        self.concentrations = concentrations
        self.chemical_names = chemical_names

    def __str__(self):
        string = self.name
        for concentration, chemical_name in zip(self.concentrations, self.chemical_names):
            string += f" {concentration} {chemical_name}"
        return string

    # TODO: two recipes that have the same ingredients and concentrations, but in different orders, should be equal.
    def __eq__(self, other):
        return self.name == other.name and self.concentrations == \
               other.concentrations and self.chemical_names == other.chemical_names



def split_concentration(string):
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
    unit = string[index:]
    return quantity, unit


def load_recipes():
    recipes = {}

    with open(recipe_library_file, "r") as file:
        for line in file:

            words = line.split()

            name = words[0]
            concentrations = []
            chemical_names = []

            for index in range(1, len(words[1:]), 2):
                concentrations.append(words[index])
                chemical_names.append(words[index+1])

            recipe = Recipe(name, concentrations, chemical_names)
            recipes[name] = recipe

    return recipes


def add_recipe(name, concentrations, chemical_names):
    recipes = load_recipes()
    if name in recipes:
        # TODO: prompt user to edit/delete/rename entry.
        print(f"Name collision: '{name}' already exists in recipe library.")
        exit()

    new_recipe = Recipe(name, concentrations, chemical_names)

    with open(recipe_library_file, "a") as file:
        file.write(str(new_recipe) + "\n")
