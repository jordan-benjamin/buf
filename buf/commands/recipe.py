# File name: recipe.py
# Author: Jordan Juravsky
# Date created: 31-07-2018

"""Module for manipulating one's library of buffer/solution recipes."""

from buf import unit, user_input, error_messages, libraries
from buf.commands import chemical
from typing import Sequence
import os
import tabulate

instructions = """buf recipe:

This subcommand allows you to access and modify your recipe library. A recipe is a description of the \
contents of a buffer or solution. It takes the form of a list of chemical names preceded by their concentrations, \
for example '300mM NaCl 10% glycerol'. Developing a library of your frequently used recipes is useful, allowing you \
to skip the listing of a solution's contents when making it (see 'buf make').

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

To view the contents of a recipe, use 'buf recipe <recipe_name>'. To view all the recipes in your library, use 'buf recipe'.
"""

recipe_library_file = libraries.fetch_library_file_path("recipes.txt")

def recipe(options: dict):
    """Parses command line options, calling the appropriate functions."""
    if options["-a"]:
        if options["<file_name>"]:
            add_recipes_from_file(options["<file_name>"])
        else:
            add_single_recipe(options["<recipe_name>"], options["<concentrations>"], options["<chemical_names>"])
    elif options["-d"]:
        delete_recipe(options["<recipe_name>"], prompt_for_confirmation= not options["--confirm"])
    elif options["<recipe_name>"]:
        display_recipe_information(options["<recipe_name>"])
    else:
        display_recipe_library()

# --------------------------------------------------------------------------------
# ----------------------------RECIPE DEFINITION AND CREATION----------------------
# --------------------------------------------------------------------------------

class Recipe:
    """Record storing a recipe's name as well as its contents, given by two lists or chemical names and concentrationss.
    For example, to make a recipe with the contents '2M NaCl 10% glycerol', the concentrations list would be ["2M", "10"]
    and the chemical_names list would be ["NaCl", "glycerol"]"""
    def __init__(self, name: str, concentrations: Sequence[str], chemical_names: Sequence[str]):

        self.name = name
        self.concentrations = concentrations
        self.chemical_names = chemical_names

    def get_contents(self):
        """Returns a list of tuples, with the format of each tuple being (chemical_concentration, chemical_name)."""
        return [(concentration, chemical_name) for concentration, chemical_name in zip(self.concentrations, self.chemical_names)]

    def get_contents_string(self):
        """Returns the contents of the recipe as a string, e.g. '2M NaCl 10% glycerol'."""
        string = str(self.concentrations[0]) + " " + str(self.chemical_names[0])
        for concentration, chemical_name in zip(self.concentrations[1:], self.chemical_names[1:]):
            string += " " + str(concentration) + " " + str(chemical_name)
        return string

    def __str__(self):
        string = self.name
        for concentration, chemical_name in zip(self.concentrations, self.chemical_names):
            string += " " + str(concentration) + " " + str(chemical_name)
        return string

    def __eq__(self, other):
        return self.name == other.name and set(self.get_contents()) == set(other.get_contents())

def assert_recipe_validity(recipe_object: Recipe, chemical_library: dict = None, recipe_library: dict = None,
                           check_existing_chemicals: bool = True):

    """Checks that a given Recipe object is valid (i.e. all concentration have both valid magnitudes and units,
     the chemicals specified in the recipe are in the chemical library if their concentration is specified in molar,
     and that a recipe with the same name doesn't already exist in the recipe library)."""

    if chemical_library == None and check_existing_chemicals == True:
        chemical_library = chemical.load_chemicals()
    if recipe_library == None:
        recipe_library = load_recipes()

    if recipe_object.name in recipe_library:
        error_messages.recipe_already_exists(recipe_object.name)

    if " " in recipe_object.name:
        error_messages.spaces_in_recipe_name(recipe_object.name)

    for concentration, chemical_name in zip(recipe_object.concentrations, recipe_object.chemical_names):

        magnitude, symbol = unit.split_unit_quantity(concentration)

        if symbol not in unit.valid_units:
            error_messages.invalid_concentration_unit(symbol)

        if check_existing_chemicals:
            if symbol in unit.concentration_units and chemical_name not in chemical_library:
                error_messages.chemical_not_found(chemical_name)

        try:
            float_magnitude = float(magnitude)
        except:
            error_messages.non_number_concentration_magnitude(magnitude)

        if float_magnitude <= 0:
            error_messages.non_positive_concentration_magnitude(float_magnitude)


def make_safe_recipe(name: str, concentrations: Sequence[str], chemical_names : Sequence[str],
                     chemical_library: dict = None, recipe_library: dict = None, check_existing_chemicals: bool = True):
    """Type checks user input, creating a Recipe object if the input is valid."""

    new_recipe = Recipe(name, concentrations, chemical_names)

    assert_recipe_validity(new_recipe, chemical_library=chemical_library, recipe_library=recipe_library,
                           check_existing_chemicals= check_existing_chemicals)

    return new_recipe


# --------------------------------------------------------------------------------
# ----------------------------------ADDING RECIPES--------------------------------
# --------------------------------------------------------------------------------

def add_single_recipe(name: str, concentrations: Sequence[str], chemical_names: Sequence[str]):
    """Adds a single recipe to the library"""
    new_recipe = make_safe_recipe(name, concentrations, chemical_names)

    with open(recipe_library_file, "a") as file:
        file.write(str(new_recipe) + "\n")


def add_recipes_from_file(filename : str):
    """Parses specified file, adding a recipe to the library for each line in the file.
    Each line in the file should first contain the recipe's name, followed by a list of contents.
    All words should be separated by spaces. Example file:

    recipe_a 10% glycerol 2M NaCl
    recipe_b 20mM KCl 4g DTT
    """
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

            concentrations = words[1::2]
            chemical_names = words[2::2]


            new_recipe_object = make_safe_recipe(recipe_name, concentrations, chemical_names, chemical_library=existing_chemical_library,
                                          recipe_library=existing_recipe_library)

            if recipe_name in new_recipe_library:
                error_messages.duplicate_file_entry(recipe_name)

            new_recipe_library[recipe_name] = new_recipe_object

        except:
            error_messages.add_from_file_termination(line_number, erroneous_line=line.strip("\n"), upper_case_data_type="Recipes")

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
    """Displays the name and contents of a specified recipe."""
    recipe_library = load_recipes()

    if recipe_name not in recipe_library:
        error_messages.recipe_not_found(recipe_name)

    recipe_object = recipe_library[recipe_name]

    print("Recipe name:", recipe_object.name)

    print("Contents:", recipe_object.get_contents_string())

def display_recipe_library():
    """Displays the names and contents of all recipes in the library."""
    print("The recipes in your library are:")

    recipe_library = load_recipes()

    table = [(recipe_object.name, recipe_object.get_contents_string()) for recipe_object in recipe_library.values()]

    # Sorting by the recipe name, upper() is called so that all the upper case names don't precede all the lowercase ones.
    table.sort(key = lambda entry: entry[0].upper())

    print(tabulate.tabulate(table, headers=["Recipe Name", "Contents"], tablefmt="fancy_grid"))


# --------------------------------------------------------------------------------
# --------------------------READING/WRITING TO RECIPE LIBRARY---------------------
# --------------------------------------------------------------------------------

def load_recipes():
    """Loads recipe library from file."""
    recipes = {}

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

                recipe = make_safe_recipe(name, concentrations, chemical_names, recipe_library=recipes, check_existing_chemicals=False)
                recipes[name] = recipe

        return recipes
    except:
        error_messages.library_load_error(lower_case_library_name= "recipe")

def save_recipe_library(recipe_library: dict):
    """Saves recipe library to file."""
    with open(recipe_library_file, "w") as file:
        for recipe_object in recipe_library.values():
            file.write(str(recipe_object) + "\n")

def reset():
    """Wipes the library."""
    with open(recipe_library_file, "w") as file:
        pass

# --------------------------------------------------------------------------------
# -------------------------------DELETING RECIPES---------------------------------
# --------------------------------------------------------------------------------

def delete_recipe(recipe_name: str, prompt_for_confirmation: bool = True):
    """Removes a specified recipe from the library."""
    recipe_library = load_recipes()

    if recipe_name not in recipe_library:
        error_messages.recipe_not_found(recipe_name)

    if prompt_for_confirmation:
        user_input.confirm()

    del(recipe_library[recipe_name])

    save_recipe_library(recipe_library)

    print("Deletion successful.")
