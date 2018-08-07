# File name: help.py
# Author: Jordan Juravsky
# Date created: 01-08-2018

import sys
import inspect

# TODO: find a way to put this module into the list. Add to members maybe?
# TODO: create general docstring for when 'buf help' is called.

general_help_docstring = """

Welcome to buf! Here's a brief overview of the program:

buf chemical:
    Allows you to modify and add to your chemical library. 
    
    View entire chemical library: buf chemical
    View information about a specific chemical: buf chemical <chemical_name>
    
    Add a chemical: buf chemical -a <molar_mass> <chemical_names>...
    Add multiple chemicals to your library, as specified in a file: buf chemical -a <file_name>
    Nickname a chemical (attach additional names to a library entry): buf chemical -n <existing_chemical_name> <nicknames>...
    
    Delete a chemical: buf chemical -d <chemical_name> [--complete] [--confirm]


buf recipe:
    Allows you to define and edit buffer/solution recipes.
    
    View information about a specific recipe: buf recipe <recipe_name>
    
    Add a recipe: buf recipe -a <recipe_name> (<concentration> <chemical_name>)...
    Add multiple recipes to your library, as specified in a file: buf recipe -a <file_name>
    
    Delete a recipe: buf recipe -d <recipe_name> [--confirm]


buf make:
    Calculate the amount of each ingredient required to make a buffer/solution.
    
    Make an already-defined recipe: buf make <volume> <recipe_name>
    Define a recipe as you make it: buf make <volume> (<concentration> <chemical_name>)...


For detailed about a specific subcommand, use 'buf help <subcommand_name>'.
"""

from buf.commands import chemical, make, recipe

def help(options):
    if options["<subcommand_name>"]:
        subcommand = options["<subcommand_name>"]
        this_module = sys.modules[__name__]

        members = inspect.getmembers(this_module, inspect.ismodule)

        if hasattr(this_module, subcommand):
            module = getattr(this_module, subcommand)

            instructions = module.instructions

            print(instructions)

        else:
            print(f"Invalid subcommand name: '{subcommand}' is not a valid subcommand.'")
    else:
        print(general_help_docstring)