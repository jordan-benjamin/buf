# File name: help.py
# Author: Jordan Juravsky
# Date created: 01-08-2018

"""Module for accessing the documentation of buf and its subcommands."""

from buf import commands
from buf import error_messages

instructions = """

buf help:

This subcommand provides documentation/usage instruction for all buf subcommands.

To access the documentation for a specific subcommand, use 'buf help <subcommand_name>'.

For a general overview of the program, use 'buf help'.
"""

general_help_docstring = """

Welcome to buf! Here's a brief overview of the program:

buf chemical:
    Manage your chemical library. 
    
    View entire chemical library: buf chemical
    View information about a specific chemical: buf chemical <chemical_name>
    
    Add a chemical: buf chemical -a <molar_mass> <chemical_names>...
    Add multiple chemicals to your library, as specified in a file: buf chemical -a <file_name>
    
    Nickname a chemical (attach additional names to a library entry): buf chemical -n <existing_chemical_name> <nicknames>...
    
    Delete a chemical: buf chemical -d <chemical_name> [--complete] [--confirm]


buf recipe:
    Manage your library of buffer/solution recipes.
    
    View entire recipe library: buf recipe
    View information about a specific recipe: buf recipe <recipe_name>
    
    Add a recipe: buf recipe -a <recipe_name> (<concentration> <chemical_name>)...
    Add multiple recipes to your library, as specified in a file: buf recipe -a <file_name>
    
    Delete a recipe: buf recipe -d <recipe_name> [--confirm]


buf make:
    Calculate the amount of each ingredient required to make a buffer/solution.
    
    Make an already-defined recipe: buf make <volume> <recipe_name>
    Define a recipe as you make it: buf make <volume> (<concentration> <chemical_name>)...


For details about a specific subcommand, use 'buf help <subcommand_name>'.
"""

def help(options):
    """Parses command line options, finding the instructions docstring of a subcommand if the subcommand is specified, \
    otherwise printing the general help docstring of buf."""
    if options["<subcommand_name>"]:
        subcommand = options["<subcommand_name>"]

        if hasattr(commands, subcommand):
            module = getattr(commands, subcommand)

            instructions = module.instructions

            print(instructions)
        else:
            error_messages.subcommand_not_found(subcommand)

    else:
        print(general_help_docstring)