Term Discovery Evaluation
=========================

Toolbox to evaluate  Word Discovery systems.

Implements some of the metrics described in [this paper](https://core.ac.uk/download/pdf/48187287.pdf).

Basic idea: phonetically transcribed each discovered item, then apply NLP evaluations.

Installation
------------

Install the required packages using pip

```bash
pip install -r requirements.txt
```

And install the package

```bash
python setup.py build && python setup.py install
```

How To Use
----------

First, you need to read the alignments and the discovered classes first

```python
from WDE.readers.disc_reader import * 
from WDE.readers.gold_reader import *  
from WDE.measures.boundary import * 
import pkg_resources 

# get paths to alignments / discovered classes
wrd_path = pkg_resources.resource_filename( 
pkg_resources.Requirement.parse('WDE'), 
            'WDE/share/english.wrd') 
phn_path = pkg_resources.resource_filename( 
 pkg_resources.Requirement.parse('WDE'), 
 'WDE/share/english.phn') 
pairs_path = pkg_resources.resource_filename( 
 pkg_resources.Requirement.parse('WDE'),
 "WDE/share/group_clusters.class" )

# read alignments
gold = Gold(wrd_path=wrd_path, 
phn_path=phn_path) 

# read discovered
discovered = Disc(pairs_path, gold) 
```

then you can call the measures: 

```python
from WDE.measures.grouping import * 

grouping = Grouping(gold, discovered)
grouping.compute_grouping()

print(grouping.precision)
print(grouping.recall)
```


# Choices:

Silences are kept in the phone alignments and are treated as phones. They are not kept in the word alignements though
and don't count as tokens/types. TODO simplify this to add it in reader (with asserts to check correctness).


