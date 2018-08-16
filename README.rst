-------------------
Project Description
-------------------

Welcome to buf!
***************
Buf is a command line based toolkit for making chemical buffers/solutions. Tired of calculating \
how much of each chemical you need to weight out when making solutions? Buf can help. Specifically, buf:

#. Allows you to develop a chemical library, saving the molar masses of frequently used chemicals.
#. Allows you to use those chemicals to define recipes for your buffers/solutions, in which you specify the concentration of each ingredient required to make the buffer.
#. Will 'make' those recipes for you, calculating how much of each ingredient you require to produce the volume of buffer you specify.

Installation
************
To install the buf toolkit, simply use ``pip install buf``.

Getting Started
***************
To introduce you to buf, let's imagine that we want to make a solution containing 50mM NaCl, is 10% glycerol by volume, and contains a \
constant 5g of KCl, regardless of the volume of our solution. We want to make 5L of this solution.

Developing Our Chemical Library
++++++++++++++++++++++++++++++++
In our recipe, we specify the concentration of NaCl with molarity. Before buf can calculate the mass of NaCl we will need to add to
our buffer when we make it, we must first tell buf the molar mass of NaCl (58.44 g/mol) by adding the chemical \
to our library. This can be done with ``buf chemical -a 58.44 NaCl``. We don't need to tell buf about \
the molar masses of glycerol or KCl, since the amounts of those chemicals we will add to our buffer aren't dependent \
on their molar masses.

Defining Our Recipe
+++++++++++++++++++
Now that our chemical library has been defined, it is time to do the same with our recipe library. Here \
we will tell buf what we want to make. We define our recipe by giving it a name and listing its contents, \
using ``buf recipe -a best_recipe 50mM NaCl 10% glycerol 5g KCl``. Now buf knows the ingredients of our \
solution; it's finally time to make it!

Making Our Solution
+++++++++++++++++++
To calculate how much of each chemical we'll need for our 5L solution, all we need to use is ``buf make 5L best_recipe``. Buf \
will use our stored chemical and recipe libraries to calculate the required amounts of each ingredient, and display the results.

Learning More
*************
This tutorial only provides a brief overview of buf; for more details about the toolkit's usage and functionality, see ``buf help``. \
For specific information about a subcommand, see ``buf help <subcommand_name>``. Happy buffer making!

Version History
***************

- 1.0.0a1: First release of buf to Test PyPI!
- 1.0.0a6: First release to PyPI proper.
- 1.0.0a7: Improved documentation.