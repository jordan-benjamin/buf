# File name: user_input.py
# Author: Jordan Juravsky
# Date created: 06-08-2018

from sys import exit

def confirm():
    user_input = input("Are you sure? [y/n]")
    while user_input not in ["y", "n"]:
        user_input = input("Invalid input. Are you sure? [y/n]")

    if user_input == "n":
        print("Operation cancelled.")
        exit()
