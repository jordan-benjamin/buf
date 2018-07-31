# File name: chemical.py
# Author: Jordan Juravsky
# Date created: 27-07-2018

# TODO: add editing.
# TODO: make sure the relative path works.

import os
chemical_library_file = os.path.join(os.path.dirname(__file__), "../library/chemicals.txt")

from ..misc import confirm, list_print
from sys import exit

class Chemical:
    # TODO: type safety on the molar mass
    def __init__(self, molar_mass, names):
        if (type(molar_mass) not in [int, float]) and (not molar_mass.isdigit()):
            print("Invalid molar mass: Molar mass must be a number")
            exit()
        self.names = names
        self.molar_mass = float(molar_mass)
    def __repr__(self):
        # TODO: replace the name code with list_print
        string = str(self.molar_mass)
        for name in self.names:
            string += " " + name
        return string
    def __eq__(self, other):
        return self.molar_mass == other.molar_mass and set(self.names) == set(other.names)


def load_chemicals():
    with open(chemical_library_file, "r") as file:
        chemical_lines = file.readlines()

    chemicals = {}

    for line in chemical_lines:
        words = line.split()
        molar_mass = words[0]
        names = words[1:]
        chemical = Chemical(molar_mass, names)
        for name in names:
            chemicals[name] = chemical

    return chemicals


def display_chemical_information(name):
    chemicals = load_chemicals()
    if name in chemicals:
        chemical = chemicals[name]
        # TODO: fancy display
        print(f"Chemical name: {name}")

        # TODO: comment this line
        # TODO: print blank other names line if no other names, or omit line altogether?
        other_names = [item for item in chemical.names if item != name]
        if len(other_names) != 0:
            other_names_string = other_names[0]
            for other_name in other_names[1:]:
                other_names_string += ", " + other_name
            print(f"Other names: {other_names_string}")

        print(f"Molar mass: {chemical.molar_mass}")

    else:
        # TODO: prompt user to add new chemical
        print(f"Name not found: '{name}' does not currently exist in your chemical library")


def display_chemical_library():
    chemicals = load_chemicals()

    print("The chemicals in your library are:\n")

    string_format = "{:<20} {:<20}"

    print(string_format.format("Chemical Name", "Molar Mass"))

    for chemical_name in chemicals:
        print(string_format.format(chemical_name, chemicals[chemical_name].molar_mass))


def save_chemicals(chemical_dict):
    with open(chemical_library_file, "r") as file:
        for chemical in chemical_dict.values():
            file.write(str(chemical))


def add_chemical(molar_mass, names):
    chemical_dict = load_chemicals()

    for name in names:
        if name in chemical_dict:
            # TODO: prompt user to view existing chemical entry.
            # TODO: give user more options to resolve collision.
            print(f"Naming collision: '{name}' already exists in chemical library.")
            # TODO: should it print all naming collisions? this stops after only one.
            return

    new_chemical = Chemical(molar_mass, names)

    with open(chemical_library_file, "a") as file:
        file.write(str(new_chemical) + "\n")


def reset():
    with open(chemical_library_file, "w") as file:
        pass

def chemical(options):
    if options["-a"]:
        add_chemical(options["<molar_mass>"], options["<chemical_names>"])
    elif options["<chemical_name>"]:
        display_chemical_information(options["<chemical_name>"])
    else:
        display_chemical_library()
