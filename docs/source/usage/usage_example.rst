.. _usage_example:

Usage Example
~~~~~~~~~~~~~

To use, you can use the `tde/eval.py` script:

.. code-block:: bash

   python eval.py discovered_class corpus output/

or you can use the API in python

.. code-block:: python

   import pkg_resources
   from tde.readers.gold_reader import *
   from tde.readers.disc_reader import *
   wrd_path = pkg_resources.resource_filename(
               pkg_resources.Requirement.parse('tde'),
               'tde/share/mandarin.wrd')
   phn_path = pkg_resources.resource_filename(
               pkg_resources.Requirement.parse('tde'),
               'tde/share/mandarin.phn')
   
   gold = Gold(wrd_path=wrd_path,
                   phn_path=phn_path)
   
   disc_clsfile = "/path/to/discovered/file"
   
   disc = Disc(disc_clsfile, gold)
   
   from tde.measures.grouping import *
   grouping = Grouping(discovered)
   grouping.compute_grouping()
   
   print(grouping.precision)
   print(grouping.recall)

