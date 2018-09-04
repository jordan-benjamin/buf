# File name: main.py
# Author: Jordan Juravsky
# Date created: 26-07-2018

"""Entry point when calling buf from the command line, parses command line arguments and passes them to appropriate modules in buf.commands"""

from docopt import docopt
import sys

if __name__ == '__main__':
    import commands
else:
    import buf.commands as commands


# TODO: add buf reset
docstring = """
buf

Usage:
    buf --version
    buf help
    buf help <subcommand_name>
    buf chemical
    buf chemical <chemical_name>
    buf chemical -a <molar_mass> <chemical_names>...
    buf chemical -a <file_name>
    buf chemical -n <existing_chemical_name> <nicknames>...
    buf chemical -d <chemical_name> [--complete] [--confirm]
    buf recipe
    buf recipe <recipe_name>
    buf recipe -a <recipe_name> (<concentrations> <chemical_names>)...
    buf recipe -a <file_name>
    buf recipe -d <recipe_name> [--confirm]
    buf make <volume> <recipe_name>
    buf make <volume> (<concentrations> <chemical_names>)...
"""

def main():
    """Parses command line arguments, calling the correct modules/functions in turn.
    If a module is found that matches a subcommand name, the function in the module that shares
    the same name is called. For example, using the 'buf chemical <args>... [options]' subcommand
    in turn calls buf.commands.chemical.chemical, passing in the dictionary of command line options
    as a parameter."""
    options = docopt(docstring, help=False, version="1.0.0")
    for k, v in options.items():
        if v:
            if hasattr(commands, k):
                module = getattr(commands, k)
                func = getattr(module, k)
                func(options)


def line(string):
    """Simulates a command line entry."""
    sys.argv = string.split()
    main()

def reset():
    """Wipes the recipe and chemical libraries."""
    commands.chemical.reset()
    commands.recipe.reset()
