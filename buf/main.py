# File name: main.py
# Author: Jordan Juravsky
# Date created: 26-07-2018

from docopt import docopt

import sys

if __name__ == '__main__':
    import commands
else:
    import buf.commands as commands

# TODO: add nicknaming.

docstring = """
buf

Usage:
    buf help <subcommand_name>
    buf chemical
    buf chemical <chemical_name>
    buf chemical -a <molar_mass> <chemical_names>...
    buf recipe <recipe_name>
    buf recipe -a <recipe_name> (<concentration> <chemical_name>)...
    buf make <volume> <recipe_name>
    buf make <volume> (<concentration> <chemical_name>)...
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

reset()

line("buf help recipe")
line("buf chemical -a 154.25 DTT")
line("buf chemical -a 58.44 NaCl")
line("buf chemical -a 68.08 imidazole")
line("buf chemical -a 121.1 tris")
line(("buf chemical -a 74.55 KCl"))
line("buf chemical -a 210.66 Arginine Arg")
line("buf chemical -a 238.3 HEPES")
line("buf chemical -a 10 glycerol")
line("buf recipe -a wash 300mM NaCl 50mM tris 20mM imidazole")
line("buf recipe -a elution 50mM tris 300mM KCl 500mM imidazole")
line("buf recipe -a refold 50mM HEPES 250mM KCl 500mM Arg 10mM DTT 20% glycerol")
line("buf make 100mL refold")


