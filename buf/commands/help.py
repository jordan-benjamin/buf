# File name: help.py
# Author: Jordan Juravsky
# Date created: 01-08-2018

"""Module for accessing the docs of buf and its subcommands."""

from buf import commands
from buf import error_messages

instructions = """

buf help:

This subcommand provides docs/usage instruction for all buf subcommands.

To access the docs for a specific subcommand, use 'buf help <subcommand_name>'.

For a general overview of the program, use 'buf help'.

Buf's documentation can also be accessed at https://buf.readthedocs.io/en/latest/index.html.
"""

general_help_docstring = """

Welcome to buf! Here's a brief overview of the program:

buf chemical:
    Manage your chemical library. 
    
    View entire chemical library: 'buf chemical'.
    View information about a specific chemical: 'buf chemical <chemical_name>'. Ex. 'buf chemical NaCl'.
    
    Add a chemical: 'buf chemical -a <molar_mass> <chemical_names>...'. Ex. 'buf chemical -a 58.44 NaCl table_salt'.
    Add chemicals from a file: 'buf chemical -a <file_name>'. Ex. 'buf chemical -a my_file.txt'. \
See 'buf help chemical' for details on file format.
    
    Nickname a chemical (attach additional names to an existing library entry): 'buf chemical -n <existing_chemical_name> <nicknames>...'. \
Ex. 'buf chemical -n NaCl table_salt sodium_chloride'.
    
    Delete a chemical: 'buf chemical -d <chemical_name> [--complete] [--confirm]'. Ex. 'buf chemical -d NaCl'.


buf recipe:
    Manage your library of buffer/solution recipes.
    
    View entire recipe library: 'buf recipe'.
    View information about a specific recipe: 'buf recipe <recipe_name>'. Ex. 'buf recipe my_recipe'.
    
    Add a recipe: 'buf recipe -a <recipe_name> (<concentration> <chemical_name>)...'. Ex. 'buf recipe -a my_recipe 300mM NaCl 10% glycerol'.
    Add recipes from a file: 'buf recipe -a <file_name>'. Ex. 'buf recipe -a my_file.txt'. \
See 'buf help recipe' for details on file format.
    
    Delete a recipe: 'buf recipe -d <recipe_name> [--confirm]'. Ex. 'buf recipe -d my_recipe'.


buf make:
    Calculate the amount of each ingredient required to make a buffer/solution.
    
    Make an already-defined recipe: 'buf make <volume> <recipe_name>'. Ex. 'buf make 250mL my_recipe'.
    Define a recipe as you make it: 'buf make <volume> (<concentration> <chemical_name>)...'. Ex. 'buf make 2M KCl 10% glycerol'.


For details and more example usages regarding a specific subcommand, use 'buf help <subcommand_name>'. Ex. 'buf help chemical'. \
Documentation can also be accessed at https://buf.readthedocs.io/en/latest/index.html.
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