# File name: chemical.py
# Author: Jordan Juravsky
# Date created: 27-07-2018

# TODO: add editing.
# TODO: make sure the relative path works.
chemical_library_file = "../library/chemicals.txt"

class Chemical:
    # TODO: type safety on the molar mass
    def __init__(self, molar_mass, names):
        self.names = names
        self.molar_mass = int(molar_mass)
    def __repr__(self):
        string = str(self.molar_mass)
        for name in self.names:
            string += " " + name
        return string


def load_chemicals():
    with open(chemical_library_file, "r") as file:
        chemical_lines = file.readlines()

    chemicals = {}

    for line in chemical_lines:
        words = line.split(sep = " ")
        molar_mass = words[0]
        names = words[1:]
        chemical = Chemical(names, molar_mass)
        for name in names:
            chemicals[name] = chemical

    return chemicals

def display_chemical_information(name):
    chemicals = load_chemicals()
    if name in chemicals:
        chemical = chemicals[name]
    else:
        # TODO: fancy display
        print(f"Chemical name: {name}")
        print(f"Other names: {}")

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
    new_chemical = Chemical(molar_mass, names)
    with open(chemical_library_file, "a") as file:
        file.write(str(new_chemical))

def chemical(options):
    if options["-a"]:
        add_chemical(options["molar_mass"], options["names"])
    else:
