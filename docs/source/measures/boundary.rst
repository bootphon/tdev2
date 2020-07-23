.. _boundary:

Boundary Measure
~~~~~~~~~~~~~~~~

* The Boundary (precision, recall, fscore) measures if the evaluated system has
  found the correct, gold boundaries.
* (:math:`X =B_{disc}`, :math:`Y = B_{gold}`)


* They are defined by:
     \textrm{Boundary precision} &= \frac{|B_{disc}\cap B_{gold}|}{|B_{disc}|} \\
   \textrm{Boundary recall} &= \frac{|B_{disc}\cap B_{gold}|}{|B_{gold}|}

 where : 
 - :math:`B_{disc}`: the set of discovered fragment boundaries
  (boundaries are defined in terms of *i*, the index of the nearest
  phoneme boundary in the transcription if it is less than 30ms away,
  and -1 (wrong boundary) otherwise)

.. note::

   Two fragments a and b *overlap* if they share more than half of
   their temporal extension.


