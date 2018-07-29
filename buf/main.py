# File name: main.py
# Author: Jordan Juravsky
# Date created: 26-07-2018

from docopt import docopt
import inspect
import buf.commands as commands


docstring = """
buf

Usage:
    buf make <volume> <recipe_name>
    buf make <volume> (<concentration> <chemical_name>)...
    buf recipe
    buf recipe -a <recipe_name> (<concentration> <chemical_name>)...
    buf recipe -n <existing_name> <nickname>
    buf chemical
    buf chemical -a <chemical_name> <molar_mass>
    buf chemical -n <existing_name> <nickname>
    buf stats
    
    
"""

def main():
    options = docopt(docstring)
    for k, v in options.items():
        if hasattr(commands, k):
            module = getattr(commands, k)
            name_func_tuple = inspect.getmembers(module, inspect.isfunction)[0]
            func = name_func_tuple[1]
            func()