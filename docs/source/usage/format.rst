.. _format:

File Formats
~~~~~~~~~~~~

Input Format
------------

The package takes as input the same format as in the
Zero Resource Speech Challenge (zerospeech.com):


.. code-block:: bash

    Class 1:
    wav1 on1 off1
    wav2 on2 off2

    Class 2:
    wav1 on3 off3
    wav3 on4 off4
    wav2 on5 off5

The ``onset`` and ``offset`` times are expressed **in seconds**.

Note that each class must end with an empty line, including the last class of
the file. So **the file must be terminated by a blank line**.

If you want to use other input formats, you need to edit the
``read_clusters`` method in ``tde/readers/disc_reader.py``.

Alignments
----------

The package uses gold phone and words alignments to evaluate the inputs.
The alignments are stored in ``tde/share``.

The formats for the alignements is (without header):

.. code-block:: bash

   filename1 on1 off1 symbol1
   filename2 on2 off2 symbol2
   ...

Where `filename` are the names of the wavs, and `symbol` are the words or
phones.

To add your own language in the package, you need to add ``yourlang.phn`` and
``yourlang.wrd`` in ``tde/share`` and add the option in ``tde/eval.py``
(line 39).
