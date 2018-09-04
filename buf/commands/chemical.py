# File name: chemical.py
# Author: Jordan Juravsky
# Date created: 27-07-2018

"""Module for handling one's chemical library of chemicals and their molar masses."""


import os
import tabulate
from buf import user_input, error_messages, libraries
from typing import Sequence

instructions = """buf chemical:

This subcommand allows you to access and modify your chemical library, i.e. your personal \
list of chemicals and their molar masses.

Before making buffers that specify a chemical's concentration in molar, that chemical's molar \
mass must first be added to your chemical library. To do this, use 'buf -a <molar_mass> <chemical_names>...', where \
the chemical's molar mass is in g/mol. For example, after adding NaCl to your library with ``buf add -a 58.44 NaCl``, \
you can then ``buf make 2L 1M NaCl`` to calculate the mass of salt you would need to add to a 2L solution to raise the \
salt concentration to 1M (see 'buf help make' for more information on performing solution calculations).

Chemicals can have multiple names, which can be listed upon addition to your library. For example, using \
'buf chemical -a 58.44 NaCl salt' allows you use either the name 'salt' or 'NaCl' when making buffers (i.e. 'buf make 2L 1M NaCl' \
is equivalent to 'buf make 2L 1M salt', since both expressions refer to the same molar mass. 

To add additional names to an existing entry in your chemical library (also known as 'nicknaming' the chemical), use \
'buf chemical -n <existing_chemical_name> <nicknames>...'. For example, if you added NaCl to your library with 'buf chemical \
-a 58.44 NaCl', and then nicknamed the chemical with 'buf chemical -n NaCl salt table_salt', you could use any of 'NaCl', 'salt', \
or 'table_salt' to refer to the same molar mass. Note that using 'buf chemical -a 58.44 NaCl table_salt salt' is equivalent to using \
'buf chemical -a 58.44 NaCl' followed by 'buf chemical -n NaCl table_salt salt'. 
 
Another way to add chemicals to your library is by specifying a list of them in a text file. This file should contain one chemical \
per line, where the first word on each line specifies the chemical's molar mass, followed by the list of the chemical's names. Spaces should \
separate each item on a line. For example, if a file 'chemicals.txt' contains the following:

58.44 NaCl salt
68.08 Imidazole imi
74.55 KCl

Using 'buf chemical -a chemicals.txt' would add these three chemicals to your library. 

To delete a chemical, use 'buf chemical -d <chemical_name>'. By default, chemical deletion is shallow/incomplete; the same chemical \
can still be accessed through its other names after one name has been deleted. For example, if 'buf chemical -a 58.44 NaCl salt' was used to \
add a chemical to our library, and then the name 'NaCl' was deleted with 'buf chemical -d NaCl', the name 'salt' would still be bound to a molar mass
of 58.44 g/mol in your chemical library. To delete a chemical entirely (i.e. delete all its names), use the '--complete' option. Using the example \
above, 'buf chemical -d NaCl --complete' would remove both the names 'NaCl' and 'salt' from our chemical library. To skip the program \
asking you to confirm your decision, use the '--confirm' option.

To view information about a specific chemical (its molar mass and additional names), use 'buf chemical <chemical_name>'. To view your entire \
chemical library, use 'buf chemical'.
"""

chemical_library_file = libraries.fetch_library_file_path("chemicals.txt")

def chemical(options : dict):
    """Parses dictionary of command line options and calls appropriate functions."""
    if options["-a"]:
        if options["<file_name>"]:
            add_chemicals_from_file(options["<file_name>"])
        else:
            add_single_chemical(options["<molar_mass>"], options["<chemical_names>"])
    elif options["-d"]:
        delete_chemical(options["<chemical_name>"], complete_deletion=options["--complete"], prompt_for_confirmation= not options["--confirm"])
    elif options["-n"]:
        nickname_chemical(options["<existing_chemical_name>"], options["<nicknames>"])
    elif options["<chemical_name>"]:
        display_chemical_information(options["<chemical_name>"])
    else:
        display_chemical_library()

# --------------------------------------------------------------------------------
# --------------------------CHEMICAL DEFINITION AND CREATION----------------------
# --------------------------------------------------------------------------------

class Chemical:
    """A record that maps chemical names to a molar mass."""
    def __init__(self, molar_mass: float, names: Sequence[str]):
        self.molar_mass = molar_mass
        self.names = names

    def __repr__(self):
        string = str(self.molar_mass)
        for name in self.names:
            string += " " + name
        return string

    def __eq__(self, other):
        return self.molar_mass == other.molar_mass and set(self.names) == set(other.names)


def make_safe_chemical(molar_mass : str, names : list, chemical_library: dict = None):
    """Type checks user input, safely making a Chemical if input is valid."""
    if chemical_library == None:
        chemical_library = load_chemicals()

    for name in names:
        if name in chemical_library:
            error_messages.chemical_already_exists(name)

        if " " in name:
            error_messages.spaces_in_chemical_name(name)

    try:
        molar_mass = float(molar_mass)
    except:
        error_messages.non_number_molar_mass(molar_mass)


    if molar_mass <= 0:
        error_messages.non_positive_molar_mass(molar_mass)

    return Chemical(molar_mass, names)

# --------------------------------------------------------------------------------
# --------------------------------ADDING CHEMICALS--------------------------------
# --------------------------------------------------------------------------------

def add_single_chemical(molar_mass: str, names: Sequence[str]):    
    """Adds single chemical to library."""
    new_chemical = make_safe_chemical(molar_mass, names)
    with open(chemical_library_file, "a") as file:
        file.write(str(new_chemical) + "\n")

def add_chemicals_from_file(filename : str):
    """Parses specified file, adding a chemical to the library for each line in the file.
    Each line in the file should first contain the chemicals's molar mass, followed by a list of its names.
    All words should be separated by spaces. Example file:

    58.44 NaCl table_salt sodium_chloride
    74.55 KCl potassium_chloride
    """
    if os.path.isfile(filename) == False:
        error_messages.file_not_found(filename)

    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except:
        error_messages.file_read_error(filename)

    existing_chemical_library = load_chemicals()

    new_chemical_names = []
    new_chemical_objects = []

    for line_number, line in enumerate(lines):

        try:
            words = line.split()
            if len(words) == 0:
                continue
            elif len(words) < 2:
                error_messages.line_too_short_in_chemical_file(line_number)

            molar_mass = words[0]
            names = words[1:]

            new_chemical = make_safe_chemical(molar_mass, names, chemical_library=existing_chemical_library)

            for name in names:
                if name in new_chemical_names:
                    error_messages.duplicate_file_entry(name)
                new_chemical_names.append(name)

            new_chemical_objects.append(new_chemical)

        except:
            error_messages.add_from_file_termination(line_number, erroneous_line=line.strip("\n"), upper_case_data_type="Chemicals")

    with open(chemical_library_file, "a") as file:
        for new_chemical in new_chemical_objects:
            file.write(str(new_chemical) + "\n")

    print("Added the following chemicals to your library:", *new_chemical_names)

# --------------------------------------------------------------------------------
# -------------------------NICKNAMING/DELETING CHEMICALS--------------------------
# --------------------------------------------------------------------------------

def nickname_chemical(existing_chemical_name: str, new_names: Sequence[str]):
    """Adds additional names to an existing chemical in the library."""
    chemical_library = load_chemicals()

    if existing_chemical_name not in chemical_library:
        error_messages.chemical_not_found(existing_chemical_name)

    for new_name in new_names:
        if new_name in chemical_library:
            error_messages.chemical_already_exists(new_name)
        if " " in new_name:
            error_messages.spaces_in_chemical_name(new_name)

    chemical_object = chemical_library[existing_chemical_name]

    chemical_object.names += new_names

    save_chemical_library(chemical_library)

def delete_chemical(chemical_name: str, complete_deletion: bool = False, prompt_for_confirmation: bool = True):
    """Deletes chemical from the library. If complete_deletion == False, only the specific name specified is deleted from \
    the library. If true, then the entire chemical record (including all other names) is deleted."""
    chemical_library = load_chemicals()

    if chemical_name not in chemical_library:
        error_messages.chemical_not_found(chemical_name)

    chemical_object = chemical_library[chemical_name]

    if complete_deletion:
        names = chemical_object.names

        if prompt_for_confirmation:
            print("You are about to delete the following chemicals from your library:", *names)
            user_input.confirm()

        for name in names:
            del (chemical_library[name])

    else:

        if prompt_for_confirmation:
            print("You are about to delete '" + str(chemical_name) + "' from your chemical library.")
            user_input.confirm()

        chemical_object.names.remove(chemical_name)
        del (chemical_library[chemical_name])

    save_chemical_library(chemical_library)

    print("Deletion successful.")

# --------------------------------------------------------------------------------
# ------------------------READING/WRITING TO CHEMICAL LIBRARY---------------------
# --------------------------------------------------------------------------------

def save_chemical_library(chemical_library: dict):
    """Saves chemical_library to file."""
    unique_chemical_objects = []

    for chemical_object in chemical_library.values():
        if chemical_object not in unique_chemical_objects:
            unique_chemical_objects.append(chemical_object)

    with open(chemical_library_file, "w") as file:
        for chemical_object in unique_chemical_objects:
            file.write(str(chemical_object) + "\n")


def load_chemicals():
    """Loads chemical library from file."""
    try:
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
    except:
        error_messages.library_load_error(lower_case_library_name="chemical")

def reset():
    """Wipes chemical library."""
    with open(chemical_library_file, "w") as file:
        pass

# --------------------------------------------------------------------------------
# -----------------------------DISPLAYING CHEMICALS-------------------------------
# --------------------------------------------------------------------------------

def display_chemical_information(chemical_name: str):
    """Displays the names and molar mass of a specified chemical."""
    chemical_library = load_chemicals()

    if chemical_name not in chemical_name:
        error_messages.chemical_not_found(chemical_name)

    chemical_object = chemical_library[chemical_name]

    print("Chemical name: " + str(chemical_name))

    other_names = [name for name in chemical_object.names if name != chemical_name]
    print("Other names:", *other_names)

    print("Molar mass: " + str(chemical_object.molar_mass))



def display_chemical_library():
    """Displays all chemicals in the library."""
    chemical_library = load_chemicals()

    print("The chemicals in your library are:")

    table = []

    for chemical_name, chemical_object in chemical_library.items():
        table.append((chemical_name, chemical_object.molar_mass))

    # Sorting by the chemical name, upper() is called so that all the upper case names don't precede all the lowercase ones.
    table.sort(key=lambda entry: entry[0].upper())

    print(tabulate.tabulate(table, headers=["Chemical Name", "Molar Mass (g/mol)"], tablefmt="fancy_grid"))
