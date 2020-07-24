.. _ned_coverage:

NED and Coverage Measure
~~~~~~~~~~~~~~~~~~~~~~~~

Many spoken term discovery systems incorporate a step whereby
fragments of speech are realigned and compared. Matching quality
measures the accuraty of this process. Here, we use the *NED/Coverage*
metrics for evaluating that.


*NED* and *Coverage* are quick to compute and give a qualitative
estimate of the matching step. *NED* is the Normalised Edit Distance;
it is equal to zero when a pair of fragments have exactly the same
transcription, and 1 when they differ in all phonemes. *Coverage* is
the fraction of corpus that contain matching pairs that has been
discovered.

.. math::

   \textrm{NED} &= \sum_{\langle x, y\rangle \in P_{disc}}
   \frac{\textrm{ned}(x, y)}{|P_{disc}|} \\
   \textrm{Coverage} &= \frac{|\textrm{cover}(P_{disc})|}{|\textrm{cover}(P_{all})|}

where

.. math::

   \textrm{ned}(\langle i, j \rangle, \langle k, l \rangle) &=
   \frac{\textrm{Levenshtein}(T_{i,j}, T_{k,l})}{\textrm{max}(j-i+1,k-l+1)} \\
   \textrm{cover}(P) &= \bigcup_{\langle i, j \rangle \in \textrm{flat}(P)}[i, j] \\
   \textrm{flat}(P) &= \{p|\exists q:\{p,q\}\in P\}


with
- :math:`P_{all}`: the set of all possible non overlapping matching
  fragment pairs. :math:`P_{all}=\{ \{a,b \}\in F_{all} \times F_{all}
  | T_{a} = T_{b}, \neg \textrm{overlap}(a,b)\}`.
- :math:`P_{disc}`: the set of non overlapping discovered pairs,
  :math:`P_{disc} = \{ \{a,b\} | a \in c, b \in c, \neg
  \textrm{overlap}(a,b), c \in C_{disc} \}`

- :math:`P_{disc^*}`: the set of pairwise substring completion of
  :math:`P_{disc}`, which mean that we compute all of the possible
  minimal path realignments of the two strings, and extract all of the
  substrings pairs along the path (e.g., for fragment pair

