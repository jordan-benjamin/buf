# File name: libraries.py
# Author: Jordan Juravsky
# Date created: 22-08-2018

"""Module for creating and accessing the files in one's library."""

import sys
import os

# Library directory is relative to sys.prefix, so that each virtual environment will have it's own library.
# This directory is not created when the package is installed because upgrading buf would then reset one's library.
library_dir = os.path.join(sys.prefix, "buf-library")

def make_library_dir():
    """Makes the buf-library directory, where all library files are stored."""
    if os.path.exists(library_dir):
        raise IsADirectoryError("Library directory '" + str(library_dir) + "' already exists.")

    os.mkdir(library_dir)

    print("Created library directory at " + str(library_dir))

def ensure_library_dir_exists():
    """Creates library_dir if it doesn't exist."""
    if os.path.exists(library_dir) == False:
        make_library_dir()

def add_library_file(file_name: str):
    """Creates a file in the library directory with the specified file name."""
    ensure_library_dir_exists()

    file_path = os.path.join(library_dir, file_name)

    if os.path.exists(file_name):
        raise FileExistsError("File at '" + str(file_path) + "' already exists.")

    with open(file_path, "w"):
        pass

    print("Created library file at '" + str(file_path) + "'.")

def fetch_library_file_path(file_name: str):
    """Gets the path to the library file passed as an argument, creating the file if it doesn't exist."""
    file_path = os.path.join(library_dir, file_name)

    if os.path.exists(file_path) == False:
        add_library_file(file_name)

    return file_path

def reset():
    """Deletes the library directory."""
    if os.path.exists(library_dir):
        os.rmdir(library_dir)