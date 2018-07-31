# File name: misc.py
# Author: Jordan Juravsky
# Date created 28-07-2018

def confirm():
    message = "Confirm? [y/n]"
    mappings = {"y" : True, "n" : False}
    user_input = input(message)

    while user_input not in mappings:
        user_input = input("Invalid response. Please answer 'y' or 'n'.")

    return mappings[user_input]

def list_print(list_to_print, sep = " "):
    if len(list_to_print) == 0:
        return ""
    string = str(list_to_print[0])
    for item in list_to_print[1:]:
        string += sep + item
    return string