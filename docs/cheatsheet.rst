Quick Reference / Cheatsheet
=============================

Welcome to the buf quick reference / cheatsheet! Below are all the commands you can use in buf, with example usages.

buf chemical
++++++++++++
Manage your chemical library (see :doc:`here <chemical>` for details).

* View entire chemical library: ``buf chemical``.
* View information about a specific chemical: ``buf chemical <chemical_name>``. Ex. ``buf chemical NaCl``.
* Add a chemical: ``buf chemical -a <molar_mass> <chemical_names>...``. Ex. ``buf chemical -a 58.44 NaCl table_salt``.
* Add multiple chemicals to your library, as specified in a file: ``buf chemical -a <file_name>``. Ex. ``buf chemical -a my_file.txt``.
* Nickname a chemical (attach additional names to an existing library entry): ``buf chemical -n <existing_chemical_name> <nicknames>...``. \
  Ex. ``buf chemical -n NaCl table_salt sodium_chloride``.
* Delete a chemical: ``buf chemical -d <chemical_name> [--complete] [--confirm]``. Ex. ``buf chemical -d NaCl``.


buf recipe
++++++++++++
Manage your library of buffer/solution recipes (see :doc:`here <recipe>` for details).

* View entire recipe library: ``buf recipe``.
* View information about a specific recipe: ``buf recipe <recipe_name>``. Ex. ``buf recipe my_recipe``.
* Add a recipe: ``buf recipe -a <recipe_name> (<concentration> <chemical_name>)...``. Ex. ``buf recipe -a my_recipe 300mM NaCl 10% glycerol``.
* Add recipes from a file: ``buf recipe -a <file_name>``. Ex. ``buf recipe -a my_file.txt``.
* Delete a recipe: ``buf recipe -d <recipe_name> [--confirm]``. Ex. ``buf recipe -d my_recipe``.


buf make
+++++++++
Calculate the amount of each ingredient required to make a buffer/solution (see :doc:`here <make>` for details).

* Calculate the amount of each ingredient required to make a buffer/solution.
* Make an already-defined recipe: ``buf make <volume> <recipe_name>``. Ex. ``buf make 250mL my_recipe``.
* Define a recipe as you make it: ``buf make <volume> (<concentration> <chemical_name>)...``. Ex. ``buf make 2M KCl 10% glycerol``.


buf help
+++++++++
Access buf documentation (see :doc:`here <help>` for details).

* See this page: ``buf help``
* See documentation for a specific subcommand: ``buf help <subcommand_name>``. Ex. ``buf help chemical``.