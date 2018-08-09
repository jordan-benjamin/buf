# File name: error_messages.py
# Author: Jordan Juravsky

# TODO: should this module be named error_messages or errors?

from sys import exit
from buf.unit import valid_units

def chemical_not_found(chemical_name: str):
    print("Chemical not found: '" + str(chemical_name) + "' does not exist in your chemical library."
          "To add a chemical to your library, use 'buf chemical -a <molar_mass> <chemical_names>...'. For "
          " more information, see 'buf help chemical'.")
    exit()

def chemical_already_exists(chemical_name: str):
    print("Chemical already exists: '" + str(chemical_name) + "' already exists in your library."
          "To delete a chemical from your library, use 'buf chemical -d <chemical_name>'. To see the "
          "chemicals in your library, use 'buf chemical'. For more information, see 'buf help chemical'.")
    exit()

def non_number_molar_mass(molar_mass: str):
    print("Invalid molar mass: '" + str(molar_mass) + "' is not a number.")
    exit()

def non_positive_molar_mass(molar_mass: float):
    print("Invalid molar mass: '" + str(molar_mass) + "' must be greater than 0.")


def recipe_not_found(recipe_name: str):
    print("Recipe not found: '" + str(recipe_name) + "' does not exist in your recipe library."
          "To add a recipe to your library, use 'buf recipe -a <recipe_name> (<chemical_concentration> <chemical_name>)...'." 
          "For more information, see 'buf help recipe'.")
    exit()

def recipe_already_exists(recipe_name: str):
    print("Recipe already exists: '" + str(recipe_name) + "' already exists in your library."
          "To delete a recipe from your library, use 'buf recipe -d <recipe_name>'. To see the "
          "recipes in your library, use 'buf recipe'. For more information, see 'buf help recipe'.")
    exit()

def invalid_concentration_unit(unit: str):
    print("Invalid unit: '" + str(unit) + "' is not a valid unit. Valid units are:", *valid_units)
    exit()

def invalid_buffer_volume_unit(unit: str):
    print("Invalid unit: '" + str(unit) + "' is not a unit of volume.")
    exit()