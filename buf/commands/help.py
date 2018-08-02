# File name: help.py
# Author: Jordan Juravsky
# Date created: 01-08-2018

import sys
import inspect

# TODO: find a way to put this module into the list. Add to members maybe?
# TODO: create general docstring for when 'buf help' is called.

if __name__ == '__main__':
    import chemical, make, recipe
else:
    from buf.commands import chemical, make, recipe

def help(options):
    subcommand = options["<subcommand_name>"]
    this_module = sys.modules[__name__]

    members = inspect.getmembers(this_module, inspect.ismodule)

    if hasattr(this_module, subcommand):
        module = getattr(this_module, subcommand)

        instructions = module.instructions

        print(instructions)

    else:
        print(f"Invalid subcommand name: '{subcommand}' is not a valid subcommand.'")