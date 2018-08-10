# File name: recipe.py
# Author: Jordan Juravsky
# Date created: 31-07-2018

from buf import unit, user_input, error_messages
from buf.commands import chemical
from sys import exit
from typing import Sequence
import os

instructions = """buf recipe:

This subcommand allows you to access and modify your recipe library. A recipe is a description of the \
contents of a buffer or solution. It takes the form of a list of chemical names preceded by their concentrations, \
for example '300mM NaCl 10% glycerol'.

Chemical concentrations can be specified in a number of ways. One common method, shown in the example above, is \
with molarity. Note that before one can specify a chemical's concentration in molar, that chemical's molar mass must \
first be added to your chemical library (see 'buf help chemical' for more information). Alternatively, one can specify \
a concentration of a chemical to be a percentage of the total volume of solution, shown above with '10% glycerol'. Lastly, \
if you want a constant mass or volume of a chemical to be added to the solution, no matter its volume, you can specify that \
constant amount in the recipe (e.g. '10g KCl'). When using these non-molar concentration, the chemical being listed does not \
need to exist in your library.

To add a recipe to your library, use 'buf recipe -a <recipe_name> (<concentration> <chemical_name>)...'. \
For example, to add the recipe specified above, use 'buf recipe -a my_recipe 300mM NaCl 10% glycerol'.

Another way to add recipes to your library is by specifying a list of them in a text file. This file should contain one recipe \
per line, where the first word on each line specifies the recipe's name, followed by the list of the recipe's contents, listing the concentration \
of each chemical before the chemical's name. Spaces should separate each item on a line. For example, if a file 'recipes.txt' \
contained the following:

buffer_a 300mM NaCl 1M KCl
buffer_b 500mM Arginine 10% glycerol

Using 'buf recipe -a recipes.txt' would add these two recipes to your library.

To delete a recipe, use 'buf recipe -d <recipe_name>'. To skip the program asking you to confirm your decision, use \
the '--confirm' option.

To view the contents of a recipe, use 'buf recipe <recipe_name>'."""

recipe_library_file = os.path.join(os.path.dirname(__file__), "../library/recipes.txt")

def recipe(options: dict):
    if options["-a"]:
        add_single_recipe(options["<recipe_name>"], options["<concentrations>"], options["<chemical_names>"])
    elif options["-d"]:
        delete_recipe(options["<recipe_name>"], options["--confirm"])
    elif options["<recipe_name>"]:
        display_recipe_information(options["<recipe_name>"])

# --------------------------------------------------------------------------------
# ----------------------------RECIPE DEFINITION AND CREATION----------------------
# --------------------------------------------------------------------------------

def make_safe_recipe(name: str, concentrations: Sequence[str], chemical_names : Sequence[str],
                     chemical_library: dict = None, recipe_library: dict = None):

    if chemical_library == None:
        chemical_library = chemical.load_chemicals()
    if recipe_library == None:
        recipe_library = load_recipes()

    # TODO: check if name is blank? will docopt let that happen?
    # TODO: ensure that docopt with guarantee that the lengths of concentrations and chemical_names are the same.
    if name in recipe_library:
        error_messages.recipe_already_exists(name)

    for concentration, chemical_name in zip(concentrations, chemical_names):

        magnitude, symbol = unit.split_unit_quantity(concentration)

        if symbol not in unit.valid_units:
            error_messages.invalid_concentration_unit(symbol)

        if symbol in unit.concentration_units and chemical_name not in chemical_library:
            error_messages.chemical_not_found(chemical_name)

        try:
            float_magnitude = float(magnitude)
        except:
            error_messages.non_number_concentration_magnitude(magnitude)

        if float_magnitude <= 0:
            error_messages.non_positive_concentration_magnitude(float_magnitude)

    return Recipe(name, concentrations, chemical_names)

class Recipe:
    def __init__(self, name: str, concentrations: Sequence[str], chemical_names: Sequence[str]):

        self.name = name
        self.concentrations = concentrations
        self.chemical_names = chemical_names

    def get_contents(self):
        return [(concentration, chemical_name) for concentration, chemical_name in zip(self.concentrations, self.chemical_names)]

    def __str__(self):
        string = self.name
        for concentration, chemical_name in zip(self.concentrations, self.chemical_names):
            string += " " + str(concentration) + " " + str(chemical_name)
        return string

    # TODO: two recipes that have the same ingredients and concentrations, but in different orders, should be equal.
    def __eq__(self, other):
        return self.name == other.name and set(self.get_contents()) == set(other.get_contents())

# --------------------------------------------------------------------------------
# ----------------------------------ADDING RECIPES--------------------------------
# --------------------------------------------------------------------------------

def add_single_recipe(name: str, concentrations: Sequence[str], chemical_names: Sequence[str]):

    new_recipe = make_safe_recipe(name, concentrations, chemical_names)

    with open(recipe_library_file, "a") as file:
        file.write(str(new_recipe) + "\n")


def add_recipes_from_file(filename : str):
    if os.path.isfile(filename) == False:
        error_messages.file_not_found(filename)

    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except:
        error_messages.file_read_error(filename)

    existing_chemical_library = chemical.load_chemicals()
    existing_recipe_library = load_recipes()

    new_recipe_library = {}

    for line_number, line in enumerate(lines):

        try:
            words = line.split()
            if len(words) == 0:
                continue
            elif len(words) < 3:
                error_messages.line_too_short_in_recipe_file(line_number)
            elif len(words) % 2 == 0:
                error_messages.line_has_inequal_contents_in_recipe_file(line_number)

            recipe_name = words[0]

            # TODO: is this readable?
            concentrations = [words[i] for i in range(1, len(words), 2)]
            chemical_names = [words[i] for i in range(2, len(words), 2)]


            new_recipe_object = make_safe_recipe(recipe_name, concentrations, chemical_names, chemical_library=existing_chemical_library,
                                          recipe_library=existing_recipe_library)

            if recipe_name in new_recipe_library:
                error_messages.duplicate_file_entry(recipe_name)

            new_recipe_library[recipe_name] = new_recipe_object

        except:
            error_messages.add_from_file_termination(line_number, upper_case_data_type="Recipes")

    with open(recipe_library_file, "a") as file:
        # Note: dict.values() can be used here but not in chemical.add_chemicals_from_file, since chemicals can
        # have multiple names, and therefore will appear multiple times in values()
        for new_recipe in list(new_recipe_library.values()):
            file.write(str(new_recipe) + "\n")

    print("Added the following recipes to your library:", *list(new_recipe_library.keys()))

# --------------------------------------------------------------------------------
# --------------------------------DISPLAYING RECIPES------------------------------
# --------------------------------------------------------------------------------

def display_recipe_information(recipe_name: str):
    recipe_library = load_recipes()

    if recipe_name not in recipe_library:
        error_messages.recipe_not_found(recipe_name)

    recipe_object = recipe_library[recipe_name]

    print("Recipe name: " + str(recipe_object))
    print("Contents:", *[str(concentration) + " " + str(chemical_name) for concentration,
                                                    chemical_name in zip(recipe_object.concentrations, recipe_object.chemical_names)])

# --------------------------------------------------------------------------------
# --------------------------READING/WRITING TO RECIPE LIBRARY---------------------
# --------------------------------------------------------------------------------

def load_recipes():
    recipes = {}
    chemical_library = chemical.load_chemicals()

    try:
        with open(recipe_library_file, "r") as file:
            for line in file:

                words = line.split()

                name = words[0]
                concentrations = []
                chemical_names = []

                for index in range(1, len(words[1:]), 2):
                    concentrations.append(words[index])
                    chemical_names.append(words[index+1])

                recipe = make_safe_recipe(name, concentrations, chemical_names, chemical_library=chemical_library, recipe_library=recipes)
                recipes[name] = recipe

        return recipes
    except:
        error_messages.library_load_error(lower_case_library_name= "recipe")

def save_recipe_library(recipe_library: dict):
    with open(recipe_library_file, "w") as file:
        for recipe_object in recipe_library.values():
            file.write(str(recipe_object) + "\n")

def reset():
    with open(recipe_library_file, "w") as file:
        pass

# --------------------------------------------------------------------------------
# -------------------------------DELETING RECIPES---------------------------------
# --------------------------------------------------------------------------------

def delete_recipe(recipe_name: str, prompt_for_confirmation: bool = True):
    recipe_library = load_recipes()

    if recipe_name not in recipe_library:
        error_messages.recipe_not_found(recipe_name)

    if prompt_for_confirmation:
        user_input.confirm()

    del(recipe_library[recipe_name])

    save_recipe_library(recipe_library)
