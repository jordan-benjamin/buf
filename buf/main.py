# File name: main.py
# Author: Jordan Juravsky
# Date created: 26-07-2018

from docopt import docopt

import sys

from tempfile import NamedTemporaryFile

if __name__ == '__main__':
    import commands
else:
    import buf.commands as commands

# TODO: is "confirm" the right name for the option that skips checking if the user is sure? Maybe --skip-check or something?
# TODO: write a better help docstring for when someone types "buf help"
# TODO: create some sort of display_recipe_library option?
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
    buf recipe <recipe_name>
    buf recipe -a <recipe_name> (<concentrations> <chemical_names>)...
    buf recipe -a <file_name>
    buf recipe -d <recipe_name> [--confirm]
    buf make <volume> <recipe_name>
    buf make <volume> (<concentrations> <chemical_names>)...
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
