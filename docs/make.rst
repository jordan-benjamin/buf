buf make
========

Subcommand Description
++++++++++++++++++++++
``buf make`` calculates the amount of each chemical that is required \
to make a solution/buffer of a given volume.

Using Your Recipe Library
+++++++++++++++++++++++++
To make a solution using a previously defined recipe (see :doc:`buf recipe <recipe>`), \
use ``buf make <volume> <recipe_name>``. For example, to make 2L of a buffer named 'wash', \
(where 'wash' has already been defined with ``buf recipe -a ...``), use ``buf make 2L wash``. The volume of the buffer \
does not need to be specified only in litres, for example ``buf make 250mL wash`` would be acceptable as well.

Defining a Recipe as it is Made
+++++++++++++++++++++++++++++++
Alternatively, one can define a solution on the spot, with ``buf make <volume> (<concentration> <chemical_name>)...``.
For example, 'buf make 0.5L 300mM NaCl 10% glycerol'. Note that in this case, the molar mass of NaCl
must already be stored in your chemical library (see :doc:`buf chemical <chemical>`).

A Note on Copying Tables
++++++++++++++++++++++++
If one wishes to copy and paste a table outputted by ``buf make`` (for example, into a text file to print), \
make sure that one uses the font 'New Courier', in order for the table to be formatted properly.