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

then you can compute the measures using the eval.py script

```bash
python eval.py discovered_class output/
```

or using the python API

```python
import pkg_resources 
from WDE.readers.gold_reader import *
from WDE.readers.disc_reader import *
wrd_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/mandarin.wrd')
phn_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/mandarin.phn')

gold = Gold(wrd_path=wrd_path, 
                phn_path=phn_path) 

disc_clsfile = "/path/to/discovered/file"

disc = Disc(disc_clsfile, gold) 

from WDE.measures.grouping import * 
grouping = Grouping(discovered)
grouping.compute_grouping()

print(grouping.precision)
print(grouping.recall)
```


