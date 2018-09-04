buf chemical
------------


Subcommand Description
++++++++++++++++++++++
``buf chemical`` allows you to access and modify your chemical library, i.e. your personal \
list of chemicals and their molar masses. Before making solutions that specify a chemical's concentration in molar, that chemical's molar \
mass must first be added to your chemical library.


Adding Chemicals
++++++++++++++++
To add a chemical to your library, use ``buf -a <molar_mass> <chemical_names>...``, where \
the chemical's molar mass is in g/mol. For example, after adding NaCl to your library with ``buf add -a 58.44 NaCl``, \
you can then ``buf make 2L 1M NaCl`` to calculate the mass of salt you would need to add to a 2L solution to raise the \
salt concentration to 1M (see :doc:`buf make <make>` for more information on performing solution calculations).

Chemicals can have multiple names, which can be listed upon addition to your library. For example, \
using ``buf chemical -a 58.44 NaCl salt`` allows you use either the name 'salt' or 'NaCl' when making buffers (i.e. ``buf make 2L 1M NaCl`` \
is equivalent to ``buf make 2L 1M salt``, since both expressions refer to the same molar mass.


Nicknaming Chemicals
++++++++++++++++++++
To add additional names to an existing entry in your chemical library (also known as 'nicknaming' the chemical), \
use ``buf chemical -n <existing_chemical_name> <nicknames>...``. For example, if you added NaCl to your library \
with ``buf chemical -a 58.44 NaCl``, and then nicknamed the chemical with ``buf chemical -n NaCl salt table_salt``, \
you could use any of 'NaCl', 'salt', or 'table_salt' to refer to the same molar mass. Note that \
using ``buf chemical -a 58.44 NaCl table_salt salt`` is equivalent to using ``buf chemical -a 58.44 NaCl`` followed \
by ``buf chemical -n NaCl table_salt salt``.


Adding Chemicals From a Text File
+++++++++++++++++++++++++++++++++
Another way to add chemicals to your library is by specifying a list of them in a text file. This file should contain one chemical \
per line, where the first word on each line specifies the chemical's molar mass, followed by the list of the chemical's names. Spaces should \
separate each item on a line. For example, if a file 'chemicals.txt' contains the following::

  58.44 NaCl salt
  68.08 Imidazole imi
  74.55 KCl

Using ``buf chemical -a chemicals.txt`` would add these three chemicals to your library.

Deleting Chemicals
++++++++++++++++++
To delete a chemical, use ``buf chemical -d <chemical_name>``. By default, chemical deletion is shallow/incomplete; the same chemical \
can still be accessed through its other names after one name has been deleted. For example, if ``buf chemical -a 58.44 NaCl salt`` was used to \
add a chemical to our library, and then the name 'NaCl' was deleted with ``buf chemical -d NaCl``, the name 'salt' would still be bound to a molar mass
of 58.44 g/mol in your chemical library. To delete a chemical entirely (i.e. delete all its names), use the ``--complete`` option. Using the example \
above, ``buf chemical -d NaCl --complete`` would remove both the names 'NaCl' and 'salt' from our chemical library. To skip the program \
asking you to confirm your decision, use the ``--confirm`` option.

Viewing Your Library
++++++++++++++++++++
To view information about a specific chemical (its molar mass and additional names), use ``buf chemical <chemical_name>``. To view your entire \
chemical library, use ``buf chemical``.