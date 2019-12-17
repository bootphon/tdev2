Word Discovery Evaluation
=========================

Toolbox to evaluate  Word Discovery systems.

Implements some of the metrics described in [this paper](https://core.ac.uk/download/pdf/48187287.pdf).

Basic idea: phonetically transcribed each discovered item, then apply NLP evaluations.

# Choices:

Silences are kept in the phone alignments and are treated as phones. They are not kept in the word alignements though
and don't count as tokens/types
