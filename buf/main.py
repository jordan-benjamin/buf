# File name: main.py
# Author: Jordan Juravsky
# Date created: 26-07-2018

from docopt import docopt

import sys

import tabulate

if __name__ == '__main__':
    import commands
else:
    import buf.commands as commands

# TODO: add nicknaming.

docstring = """
buf

Usage:
    buf chemical
    buf chemical <chemical_name>
    buf chemical -a <molar_mass> <chemical_names>...
    buf recipe <recipe_name>
    buf recipe -a <recipe_name> (<concentration> <chemical_name>)...
    buf make <volume> <recipe_name>
    buf make <volume> (<concentration> <chemical_name>)...
"""

def main():
    options = docopt(docstring)
    #print(options)
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

reset()
line("buf chemical -a 100 salt")
line("buf chemical -a 200 pepper")
line("buf make 2L 3M salt 10% pepper")



