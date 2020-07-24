.. _token_boundary:

Token and Boundary Measures
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parsing quality is evaluated using two metrics. The first one (Token
precision, recall and F-score) evaluates how many of the word tokens
were correctly segmented (:math:`X = F_{disc}`, :math:`Y =
F_{goldLex}`). The second one (Boundary precision, recall and F-score)
evaluates how many of the gold word boundaries were found (:math:`X =
B_{disc}`, :math:`Y = B_{gold}`). These two metrics are typically
correlated, but researchers typically use the first. We provide
Boundary metrics for completeness, and also to enable system
diagnostic.

.. math::

   \textrm{Token precision} &= \frac{|F_{disc}\cap F_{goldLex}|}{|F_{disc}|} \\
   \textrm{Token recall} &= \frac{|F_{disc}\cap F_{goldLex}|}{|F_{goldLex}|} \\
   \textrm{Boundary precision} &= \frac{|B_{disc}\cap B_{gold}|}{|B_{disc}|} \\
   \textrm{Boundary recall} &= \frac{|B_{disc}\cap B_{gold}|}{|B_{gold}|}

where

- :math:`F_{disc}`: the set of discovered fragments,
  :math:`F_{disc} = \{ f | f \in c , c \in C_{disc} \}`
- :math:`F_{goldLex}`: the set of fragments corresponding to the
  corpus transcribed at the word level (gold transcription).
- :math:`B_{disc}`: the set of discovered fragment boundaries
  (boundaries are defined in terms of *i*, the index of the nearest
  phoneme boundary in the transcription if it is less than 30ms away,
  and -1 (wrong boundary) otherwise)
- :math:`B_{gold}`: the set of boundaries in the parsed corpus.

The details of these metrics are given in the Ludusan et al (2014)
paper. The only divergence between this paper and the present
measures, is that contrary to the paper, we compute these scores on
the entirety of the corpus, rather than on the covered corpus. It is
necessary to do this if we want to compare systems that will cover
different subsets of the corpus. In the implementation for the
challenge, we use a subsampling scheme whereby the corpus is cut into
n-equal parts and each metric is computed on each of the subsample
separately and then averaged. This enables the computation to be more
tractable, and also to provide a standard deviation measure for each
metric. We also provide, in addition to each metric ran on the entire
corpus, the same metric restricted to within talker matches. This is
to enable the evaluation of systems that are specialized in within
talker spoken term discovery.
