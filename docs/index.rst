.. buf documentation master file, created by
   sphinx-quickstart on Fri Aug  3 14:22:54 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Buf!
===============================


Project Description
-------------------
Buf is a command line based toolkit for making chemical buffers/solutions. Tired of calculating \
how much of each chemical you need to add when making solutions? Buf can help. Specifically, buf:

#. Allows you to develop a chemical library, saving the molar masses of frequently used chemicals.
#. Allows you to use those chemicals to define recipes for your buffers/solutions, in which you specify \
   the concentration of each ingredient required to make the buffer.
#. Will 'make' those recipes for you, calculating how much of each ingredient you require to produce the volume of solution you specify.

Installation
------------
To install the buf toolkit, simply use ``pip install buf``.

Documentation
-------------

To those new to the toolkit, see the :doc:`getting started <getting_started>` tutorial. For more detailed instructions \
regarding a specific subcommand of buf, see any of the following:

.. toctree::
   :maxdepth: 1

   Home <self>
   Getting Started <getting_started>
   Quick Reference / Cheatsheet <cheatsheet>
   buf chemical <chemical>
   buf recipe <recipe>
   buf make <make>
   buf help <help>
