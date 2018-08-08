# File name: recipe.py
# Author: Jordan Juravsky
# Date created: 31-07-2018

from buf import unit, user_input
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
 
To delete a recipe, use 'buf recipe -d <recipe_name>'. To skip the program asking you to confirm your decision, use \
the '--confirm' option.

To view the contents of a recipe, use 'buf recipe <chemical_name>'."""

recipe_library_file = os.path.join(os.path.dirname(__file__), "../library/recipes.txt")

# TODO: raise error if none of the options specified work (i.e. an else at the bottom of the method)?
def recipe(options: dict):
    if options["-a"] == True:
        add_single_recipe(options["<recipe_name>"], options["<concentrations>"], options["<chemical_names>"])
    elif options["-d"] == True:
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
        print(f"Name collision: '{name}' already exists in chemical library.")
        exit()

    for concentration, chemical_name in zip(concentrations, chemical_names):

        quantity, symbol = unit.split_unit_quantity(concentration)

        # TODO: accept blank unit, load from settings.
        if symbol not in unit.valid_units:
            # TODO: display all valid units?
            print(f"Invalid unit: '{symbol}' is not a valid unit.")
            exit()

        if symbol in unit.concentration_units and chemical_name not in chemical_library:
            print(f"Chemical not found: molar mass of '{chemical_name}' not in chemical library. "
                  "Before specifying a chemical's concentration with molarity, first use 'buf chemical -a "
                  "<molar_mass> <chemical_names>...' to add the chemical to your library.")
            exit()


        try:
            float_quantity = float(quantity)
        except:
            # TODO: change this message to mention numbers?
            print(f"Invalid quantity: '{quantity}' is not a valid quantity")
            exit()

        if float_quantity <= 0:
            print(f"Invalid quantity: '{float_quantity}' is not greater than 0.")
            exit()

    return Recipe(name, concentrations, chemical_names)

class Recipe:
    def __init__(self, name: str, concentrations: Sequence[str], chemical_names: Sequence[str]):

        self.name = name
        self.concentrations = concentrations
        self.chemical_names = chemical_names

    def get_contents(self):
        string = f"{self.concentrations[0]} {self.chemical_names[0]}"
        for concentration, chemical_name in zip(self.concentrations[1:], self.chemical_names[1:]):
            string += f" {concentration} {chemical_name}"
        return string

    def __str__(self):
        return self.name + " " + self.get_contents()

    # TODO: two recipes that have the same ingredients and concentrations, but in different orders, should be equal.
    def __eq__(self, other):
        return self.name == other.name and self.concentrations == \
               other.concentrations and self.chemical_names == other.chemical_names



# --------------------------------------------------------------------------------
# ----------------------------------ADDING RECIPES--------------------------------
# --------------------------------------------------------------------------------

def add_single_recipe(name: str, concentrations: Sequence[str], chemical_names: Sequence[str]):

    new_recipe = make_safe_recipe(name, concentrations, chemical_names)

    with open(recipe_library_file, "a") as file:
        file.write(str(new_recipe) + "\n")

# TODO: what's better practice? reading file lines then getting out, or iterating through the file inside the context manager?
def add_recipes_from_file(filename : str):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except:
        # TODO: tell user to specify absolute path / go to the right directory?
        print(f"File not found: '{filename}' could not be located.")

    existing_chemical_library = chemical.load_chemicals()
    existing_recipe_library = load_recipes()

    new_recipe_library = {}

    for line_number, line in enumerate(lines):

        try:
            words = line.split()
            if len(words) == 0:
                continue
            elif len(words) < 3:
                print(f"Invalid line length: line {line_number} must contain at least one concentration-chemical name pair.")
                exit()
            elif len(words) % 2 == 0:
                print(f"Invalid line length: line {line_number} contains an inequal number of concentrations and chemical names.")
                exit()

            recipe_name = words[0]

            # TODO: is this readable?
            concentrations = [words[i] for i in range(1, len(words), 2)]
            chemical_names = [words[i] for i in range(2, len(words), 2)]


            new_recipe_object = make_safe_recipe(recipe_name, concentrations, chemical_names, chemical_library=existing_chemical_library,
                                          recipe_library=existing_recipe_library)

            if recipe_name in new_recipe_library:
                print(f"Duplicate file entry: '{name}' already used earlier in file.")
                exit()


            new_recipe_library[recipe_name] = new_recipe_object

        except:
            print(f"Error encountered on line {line_number}. Recipes specified in file not added to library.")
            exit()

    with open(recipe_library_file, "a") as file:
        # Note: dict.values() can be used here but not in chemical.add_chemicals_from_file, since chemicals can
        # have multiple names, and therefore will appear multiple times in values()
        for new_recipe in list(new_recipe_library.values()):
            file.write(str(new_recipe) + "\n")

    print(f"Added the following recipes to your library:", *list(new_recipe_library.keys()))

# --------------------------------------------------------------------------------
# --------------------------------DISPLAYING RECIPES------------------------------
# --------------------------------------------------------------------------------

def display_recipe_information(recipe_name: str):
    recipe_library = load_recipes()

    if recipe_name not in recipe_library:
        print(f"Invalid recipe name: '{recipe_name}' not in recipe library.")
        exit()

    recipe_object = recipe_library[recipe_name]

    print(f"Recipe name: {recipe_object.name}")
    print(f"Contents: {recipe_object.get_contents()}")

# --------------------------------------------------------------------------------
# --------------------------READING/WRITING TO RECIPE LIBRARY---------------------
# --------------------------------------------------------------------------------

def load_recipes():
    # TODO: what if someone manually mucks up the file? check for corruption?
    recipes = {}
    chemical_library = chemical.load_chemicals()

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
        print(f"Recipe not found: '{recipe_name}' not found in recipe library.")
        exit()

    if prompt_for_confirmation:
        user_input.confirm()

    del(recipe_library[recipe_name])

    save_recipe_library(recipe_library)

