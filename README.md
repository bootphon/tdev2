Term Discovery Evaluation
=========================

Toolbox to evaluate  Term Discovery systems.

Implements some of the metrics described in [this paper](https://core.ac.uk/download/pdf/48187287.pdf).

This toolbox transcribed phoneticall each discovered interval, then applies 
NLP evaluation to judge the quality of the discovery.
The metrics are:
- NED : mean of the edit distance between all the discovered pairs
- coverage: percentage of the corpus covered
- token/type: measure how good the system was at finding gold tokens and gold types
- boundary: measure how good the system was at finding gold boundaries
- grouping: judge the purity of the clusters formed by the system

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

The discovered intervals should be in the following format:

```bash
    Class 1:
    wav1 on1 off1
    wav2 on2 off2

    Class 2:
    wav1 on3 off3
    wav3 on4 off4

```

and finish by an empty line (which is important).

You can compute the measures using the eval.py script

```bash
python eval.py discovered_class corpus output/
```

where corpus is the corpus you want to evaluate (currently supporting ['english'
, 'french', 'mandarin', 'buckeye'], where the first three are the corpora of the
ZeroSpeech 2017 challenge).

You can also use the python API

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


