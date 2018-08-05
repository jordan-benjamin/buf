# File name: chemical.py
# Author: Jordan Juravsky
# Date created: 27-07-2018

# TODO: add editing.
# TODO: make sure the relative path works.

import os

import tabulate

from sys import exit

# TODO: check if lines this wide will fit on a terminal window of default size.
instructions = """buf chemical:

This subcommand allows you to access and modify your chemical library, i.e. your personal \
list of chemicals that you use to make buffers.

To add a chemical to your library, call 'buf chemical -a <molar_mass> <chemical_names>...' \
The repeating final argument allows you to specify multiple names for the same chemical.  \
For example, calling 'buf chemical -a 58.44 NaCl salt' adds both 'NaCl' and 'salt' to your \
chemical library, both with the same molar mass."""

chemical_library_file = os.path.join(os.path.dirname(__file__), "../library/chemicals.txt")

def chemical(options : dict):

    if options["-a"]:
        if options["<file_name>"]:
            add_chemicals_from_file(options["<file_name>"])
        else:
            add_single_chemical(options["<molar_mass>"], options["<chemical_names>"])

    elif options["<chemical_name>"]:
        display_chemical_information(options["<chemical_name>"])

    else:
        display_chemical_library()

# TODO: what's better practice? reading file lines then getting out, or iterating through the file inside the context manager?
def add_chemicals_from_file(filename : str):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except:
        # TODO: tell user to specify absolute path / go to the right directory?
        print(f"File not found: '{filename}' could not be located.")

    existing_chemical_library = load_chemicals()

    new_chemical_names = []
    new_chemical_objects = []

    for line_number, line in enumerate(lines):

        try:
            words = line.split()
            if len(words) == 0:
                continue
            elif len(words) < 2:
                print(f"Invalid line length: line {line_number} must have at least one name after its molar mass.")
                exit()

            molar_mass = words[0]
            names = words[1:]


            new_chemical = make_safe_chemical(molar_mass, names, chemical_library=existing_chemical_library)

            for name in names:
                if name in new_chemical_names:
                    print(f"Duplicate file entry: '{name}' already used earlier in file.")
                    exit()
                new_chemical_names.append(name)

            new_chemical_objects.append(new_chemical)

        except:
            print(f"Error encountered on line {line_number}. Chemicals specified in file not added to library.")
            exit()

    with open(chemical_library_file, "a") as file:
        for new_chemical in new_chemical_objects:
            file.write(str(new_chemical) + "\n")

    print(f"Added the following chemicals to your library: ", *new_chemical_names)



# TODO: make sure names cannot be whitespace.
def make_safe_chemical(molar_mass : str, names : list, chemical_library: dict = None):
    if chemical_library == None:
        chemical_library = load_chemicals()

    for name in names:
        if name in chemical_library:
            print(f"Name collision: '{name}' already exists in chemical library")
            exit()

    try:
        molar_mass = float(molar_mass)
    except:
        print(f"Invalid molar mass: '{molar_mass}' is not a number.")
        exit()


    if molar_mass <= 0:
        print(f"Invalid molar mass: '{molar_mass}' must be greater than 0.")
        exit()

    return Chemical(molar_mass, names)


class Chemical:
    # TODO: type safety on the molar mass
    def __init__(self, molar_mass: float, names: list):
        self.molar_mass = molar_mass
        self.names = names

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
        chemical = make_safe_chemical(molar_mass, names, chemical_library=chemicals)
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
        print(f"Name not found: '{name}' does not currently exist in your chemical library.")

        exit()


def display_chemical_library():
    chemicals = load_chemicals()

    # TODO: delete this line?
    print("The chemicals in your library are:\n")

    table = []

    # TODO: is it more efficient to use dict.items than this?
    for chemical_name in chemicals:
        table.append([chemical_name, chemicals[chemical_name].molar_mass])

    print(tabulate.tabulate(table, headers=["Chemical Name", "Molar Mass"], tablefmt="fancy_grid"))


def add_single_chemical(molar_mass, names):
    new_chemical = make_safe_chemical(molar_mass, names)
    with open(chemical_library_file, "a") as file:
        file.write(str(new_chemical) + "\n")


def reset():
    with open(chemical_library_file, "w") as file:
        pass
