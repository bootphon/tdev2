[![Anaconda-Server Badge](https://anaconda.org/coml/tde/badges/version.svg)](
https://anaconda.org/coml/tde)

Term Discovery Evaluation
=========================

Toolbox to evaluate  Term Discovery systems.

* Complete Documentation and metrics description ar
  available at https://docs.cognitive-ml.fr/tde/

This toolbox transcribed phonetical each discovered interval, then applies
NLP evaluation to judge the quality of the discovery.
The metrics are:
- NED : mean of the edit distance between all the discovered pairs
- coverage: percentage of the corpus covered
- token/type: measure how good the system was at finding gold tokens and gold types
- boundary: measure how good the system was at finding gold boundaries
- grouping: judge the purity of the clusters formed by the system
