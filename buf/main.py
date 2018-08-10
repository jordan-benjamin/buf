# File name: main.py
# Author: Jordan Juravsky
# Date created: 26-07-2018

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

For more information, see 'buf help' or 'buf help <subcommand_name>'.
"""

def main():
    options = docopt(docstring, help=False)
    for k, v in options.items():
        if v:
            if hasattr(commands, k):
                module = getattr(commands, k)
                func = getattr(module, k)
                func(options)


def line(string):
    sys.argv = string.split()
    main()

def reset():
    commands.chemical.reset()
    commands.recipe.reset()
