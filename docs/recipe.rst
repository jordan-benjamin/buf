buf recipe
==========

Subcommand Desciption
+++++++++++++++++++++
``buf recipe`` allows you to access and modify your recipe library. A recipe is a description of the \
contents of a buffer or solution. It takes the form of a list of chemical names preceded by their concentrations, \
for example '300mM NaCl 10% glycerol'. Developing a library of your frequently used recipes is useful, allowing you \
to skip the listing of a solution's contents when making it (see :doc:`buf make <make>`).

A Note on Concentrations
------------------------
Chemical concentrations can be specified in a number of ways. One common method, shown in the example above, is \
with molarity. Note that before one can specify a chemical's concentration in molar, that chemical's molar mass must \
first be added to your chemical library (see :doc:`buf chemical <chemical>`). Alternatively, one can specify \
a concentration of a chemical to be a percentage of the total volume of solution, shown above with '10% glycerol'. Lastly, \
if you want a constant mass or volume of a chemical to be added to the solution, no matter its volume, you can specify that \
constant amount in the recipe (e.g. '10g KCl'). When using these non-molar concentration, the chemical being listed does not \
need to exist in your library.

Adding Recipes
+++++++++++++++
To add a recipe to your library, use ``buf recipe -a <recipe_name> (<concentration> <chemical_name>)...``. \
For example, to add the recipe specified above, use 'buf recipe -a my_recipe 300mM NaCl 10% glycerol'.

Adding Recipes from a Text File
++++++++++++++++++++++++++++++++
Another way to add recipes to your library is by specifying a list of them in a text file. This file should contain one recipe \
per line, where the first word on each line specifies the recipe's name, followed by the list of the recipe's contents, listing the concentration \
of each chemical before the chemical's name. Spaces should separate each item on a line. For example, if a file ``recipes.txt`` \
contained the following::

   buffer_a 300mM NaCl 1M KCl
   buffer_b 500mM Arginine 10% glycerol

Using ``buf recipe -a recipes.txt`` would add these two recipes to your library.

Deleting Recipes
++++++++++++++++
To delete a recipe, use ``buf recipe -d <recipe_name>``. To skip the program asking you to confirm your decision, use \
the ``--confirm`` option.

Viewing Your Recipe Library
+++++++++++++++++++++++++++
To view the contents of a recipe, use ``buf recipe <recipe_name>``.
To view all the recipes in your library, use ``buf recipe``.