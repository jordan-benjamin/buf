# File name: error_messages.py
# Author: Jordan Juravsky
# Date created: 08-08-2018

"""Descriptive error messages that use sys.exit to cleanly end the program without displaying a traceback."""

from sys import exit
from buf import unit

# --------------------------------------------------------------------------------
# -----------------------------------CHEMICAL ERRORS------------------------------
# --------------------------------------------------------------------------------

def chemical_not_found(chemical_name: str):
    print("Chemical not found: '" + str(chemical_name) + "' does not exist in your chemical library. "
          "To add a chemical to your library, use 'buf chemical -a <molar_mass> <chemical_names>...'. For "
          "more information, see 'buf help chemical'.")
    exit()

def chemical_already_exists(chemical_name: str):
    print("Chemical already exists: '" + str(chemical_name) + "' already exists in your library. "
          "To delete a chemical from your library, use 'buf chemical -d <chemical_name>'. To see the "
          "chemicals in your library, use 'buf chemical'. For more information, see 'buf help chemical'.")
    exit()

def non_number_molar_mass(molar_mass: str):
    print("Invalid molar mass: '" + str(molar_mass) + "' is not a number.")
    exit()

def non_positive_molar_mass(molar_mass: float):
    print("Invalid molar mass: '" + str(molar_mass) + "' must be greater than 0.")
    exit()

def line_too_short_in_chemical_file(line_number_zero_indexed: float):
    print("Invalid line length: line " + str(line_number_zero_indexed + 1) + " must contain at least one name after its molar mass. For "
          "more information, see 'buf help chemical'.")
    exit()

def spaces_in_chemical_name(chemical_name: str):
    print("Invalid chemical name: '" + str(chemical_name) + "' cannot contain spaces.")
    exit()

# --------------------------------------------------------------------------------
# ---------------------------------RECIPE ERRORS----------------------------------
# --------------------------------------------------------------------------------

def recipe_not_found(recipe_name: str):
    print("Recipe not found: '" + str(recipe_name) + "' does not exist in your recipe library.",
          "To add a recipe to your library, use 'buf recipe -a <recipe_name> (<chemical_concentration> <chemical_name>)...'.",
          "For more information, see 'buf help recipe'.")
    exit()

def recipe_already_exists(recipe_name: str):
    print("Recipe already exists: '" + str(recipe_name) + "' already exists in your library.",
          "To delete a recipe from your library, use 'buf recipe -d <recipe_name>'. To see the",
          "recipes in your library, use 'buf recipe'. For more information, see 'buf help recipe'.")
    exit()

def invalid_concentration_unit(symbol: str):
    print("Invalid unit: '" + str(symbol) + "' is not a valid unit. Valid units are:", *unit.valid_units)
    exit()

def non_number_concentration_magnitude(magnitude: str):
    print("Invalid concentration: '" + str(magnitude) + "' is not a number.")
    exit()

def non_positive_concentration_magnitude(magnitude: str):
    print("Invalid concentration: '" + str(magnitude) + "' is not greater than 0.")
    exit()

def line_too_short_in_recipe_file(line_number_zero_indexed: float):
    print("Invalid line length: line " + str(line_number_zero_indexed + 1) + " must contain at least one concentration-chemical name pair.",
          "For more information see 'buf help recipe'.")
    exit()

def line_has_inequal_contents_in_recipe_file(line_number_zero_indexed: float):
    print("Invalid line length: line " + str(line_number_zero_indexed + 1) + " contains an inequal number of concentrations and chemical names.")
    exit()

def spaces_in_recipe_name(recipe_name: str):
    print("Invalid recipe name: '" + str(recipe_name) + "' cannot contain spaces.")
    exit()

# --------------------------------------------------------------------------------
# -----------------------------------MAKE ERRORS----------------------------------
# --------------------------------------------------------------------------------

def invalid_buffer_volume_unit(symbol: str):
    print("Invalid volume unit: '" + str(symbol) + "' is not a valid unit of volume. Valid units are:", *unit.volume_units.get_symbols())
    exit()

def non_number_buffer_volume_magnitude(magnitude: str):
    print("Invalid volume: '" + str(magnitude) + "' is not a valid number.")
    exit()

def non_positive_buffer_volume_magnitude(magnitude: float):
    print("Invalid volume: '" + str(magnitude) + "' is not greater than 0.")
    exit()

# --------------------------------------------------------------------------------
# -----------------------------------HELP ERRORS----------------------------------
# --------------------------------------------------------------------------------

def subcommand_not_found(subcommand: str):
    print("Subcommand not found: '" + str(subcommand) + "' is not a valid subcommand.",
          "For an overview of all subcommands, see 'buf help'.")
    exit()

# --------------------------------------------------------------------------------
# -----------------------------------UNIT ERRORS----------------------------------
# --------------------------------------------------------------------------------

def unit_not_in_ladder(symbol: str):
    print("Invalid unit: '" + str(symbol) + "' not in ladder.")
    exit()

def unit_not_in_any_ladder(symbol: str):
    print("Invalid unit: '" + str(symbol) + "' not in any unit ladder.")
    exit()

def no_greater_unit_in_ladder(symbol: str):
    print("No greater unit: '" + str(symbol) + "' is the largest unit in its ladder.")
    exit()

def no_lesser_unit_in_ladder(symbol: str):
    print("No lesser unit: '" + str(symbol) + "' is the smallest unit in its ladder.")
    exit()

# --------------------------------------------------------------------------------
# ------------------------------FILE HANDLING ERRORS------------------------------
# --------------------------------------------------------------------------------

def file_not_found(file_name: str):
    print("File not found: '" + str(file_name) + "' could not be located.")
    exit()

def file_read_error(file_name: str):
    print("File read error: '" + str(file_name) + "' could not be read.")
    exit()

def duplicate_file_entry(name: str):
    print("Duplicate file entry: '" + str(name) + "' already used earlier in the file.")
    exit()

def library_load_error(lower_case_library_name: str):
    print("Library load error: unable to load " + str(lower_case_library_name) + " library. Possible file corruption.")
    exit()

# Data type refers to chemicals or recipes.
def add_from_file_termination(line_number_zero_indexed: str, erroneous_line: str, upper_case_data_type: str):
    print("Error encountered on line " + str(line_number_zero_indexed + 1) + ": '" + str(erroneous_line) + "'. " + str(upper_case_data_type) +
          " specified in file not added to library.")
    exit()