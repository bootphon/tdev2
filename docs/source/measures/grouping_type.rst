.. _grouping_type:

Grouping and Type Measures
~~~~~~~~~~~~~~~~~~~~~~~~~~

Clustering quality is evaluated using two metrics. The first metrics
(Grouping precision, recall and F-score) computes the intrinsic
quality of the clusters in terms of their phonetic composition. This
score is equivalent to the purity and inverse purity scores used for
evaluating clustering. As the Matching score, it is computed over
pairs, but contrary to the Matching scores, it focusses on the covered
part of the corpus.

.. math::

   \textrm{Grouping precision} &= \sum_{t\in\textrm{types}(\textrm{flat}(P_{clus}))}
   freq(t, P_{clus})
   \frac{|\textrm{match}(t, P_{clus} \cap P_{goldclus})|}{|\textrm{match}(t, P_{clus})|} \\
   \textrm{Grouping recall} &= \sum_{t\in\textrm{types}(\textrm{flat}(P_{goldclus}))}
   freq(t, P_{goldclus})
   \frac{|\textrm{match}(t, P_{clus} \cap P_{goldclus})|}{|\textrm{match}(t, P_{goldclus})|}

where

.. math::
   P_{clus} &= \{\langle \langle i, j\rangle , \langle k, l \rangle\rangle
   | &\exists c\in C_{disc},\langle i, j\rangle\in c \wedge \langle k, l\rangle\in c\} \\
   P_{goldclus} &= \{\langle \langle i, j\rangle , \langle k, l \rangle\rangle
   | &\exists c_1,c_2\in C_{disc}:\langle i, j\rangle\in c_1 \wedge \langle k, l\rangle\in c_2 \\
   && \wedge T_{i,j}=T_{k,l} \wedge [i,j] \cap [k,l] = \varnothing \}


The second metrics (Type precision, recall and F-score) takes as the
gold cluster set the true lexicon and is therefore much more
demanding. Indeed, a system could have very pure clusters, but could
systematically missegment words. Since a discovered cluster could have
several transcriptions, we use all of them (rather than using some
kind of centroid).

.. math::

   \textrm{Type precision} &= \frac{|\textrm{types}(F_{disc}) \cap \textrm{types}(F_{goldLex})|}
   {|\textrm{types}(F_{disc})|} \\
   \textrm{Type recall} &= \frac{|\textrm{types}(F_{disc}) \cap \textrm{types}(F_{goldLex})|}
   {|\textrm{types}(F_{goldLex})|} \\

where

- :math:`F_{disc}`: the set of discovered fragments,
  :math:`F_{disc} = \{ f | f \in c , c \in C_{disc} \}`
- :math:`F_{goldLex}`: the set of fragments corresponding to the
  corpus transcribed at the word level (gold transcription).

