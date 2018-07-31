# File name: main.py
# Author: Jordan Juravsky
# Date created: 26-07-2018

from docopt import docopt

if __name__ == '__main__':
    import commands
else:
    import buf.commands as commands


docstring = """
buf

Usage:
    buf chemical
    buf chemical <chemical_name>
    buf chemical -a <molar_mass> <chemical_names>...
    buf chemical -n <existing_name> <new_names>...
"""

def main():
    options = docopt(docstring)
    for k, v in options.items():
        if hasattr(commands, k):
            module = getattr(commands, k)
            func = getattr(module, k)
            func()