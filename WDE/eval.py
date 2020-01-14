#!/usr/bin/env python
import argparse
import pkg_resources 

from WDE.measures.ned import *
from WDE.measures.boundary import *
from WDE.measures.grouping import *
from WDE.measures.coverage import *
from WDE.measures.token_type import *
from WDE.readers.gold_reader import *
from WDE.readers.disc_reader import *

def main():
    parser = argparse.ArgumentParser(
        prog='TDE',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Evaluate spoken term discovery',
        epilog="""Example usage:
    
    $ ./english_eval2 my_sample.classes resultsdir/
    
    evaluates STD output `my_sample.classes` on the english dataset and stores the
    output in `resultsdir/`.
    
    Classfiles must be formatted like this:
    
    Class 1 (optional_name)
    fileID starttime endtime
    fileID starttime endtime
    ...
    
    Class 2 (optional_name)
    fileID starttime endtime
    ...
    """)
    parser.add_argument('disc_clsfile', metavar='discovered', type=str)
    parser.add_argument('--measures', '-m',
                        nargs='*',
                        default=[],
                        choices=['boundary', 'grouping', 
                                 'token/type', 'coverage',
                                 'ned'])
    parser.add_argument('output', type=str,
                        help="path in which to write the output")

    args = parser.parse_args()
    wrd_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/english.wrd')
    phn_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/english.phn')
   
    gold = Gold(wrd_path=wrd_path, 
                phn_path=phn_path) 

    disc = Disc(args.disc_clsfile, gold) 

    measures = args.measures
    output = args.output
    if len(measures) == 0 or "boundary" in measures:
        boundary = Boundary(gold, disc, output)
        boundary.compute_boundary()
        boundary.write_score()
    if len(measures) == 0 or "grouping" in measures:
        grouping = Grouping(disc, output)
        grouping.compute_grouping()
        grouping.write_score()
    if len(measures) == 0 or "token/type" in measures:
        token_type = TokenType(gold, disc, output)
        token_type.compute_token_type()
        token_type.write_score()
    if len(measures) == 0 or "coverage" in measures:
        coverage = Coverage(gold, disc, output)
        coverage.compute_coverage()
        coverage.write_score()
    if len(measures) == 0 or "ned" in measures:
        ned = Ned(disc, output)
        ned.compute_ned()
        ned.write_score()

    
if __name__ == "__main__": 
    main()
