#!/usr/bin/env python
import time
import argparse
import pkg_resources 

from tdev2.measures.ned import *
from tdev2.measures.boundary import *
from tdev2.measures.grouping import *
from tdev2.measures.coverage import *
from tdev2.measures.token_type import *
from tdev2.readers.gold_reader import *
from tdev2.readers.disc_reader import *

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
    parser.add_argument('corpus', metavar='language', type=str, 
                        choices=['buckeye', 'english', 'french',
                                 'mandarin'],
                        help='Choose the corpus you want to evaluate')
    parser.add_argument('--measures', '-m',
                        nargs='*',
                        default=[],
                        choices=['boundary', 'grouping', 
                                 'token/type', 'coverage',
                                 'ned'])
    parser.add_argument('--njobs', '-n',
                        default=1,
                        type=int,
                        help="number of cpus to be used in grouping")
    parser.add_argument('output', type=str,
                        help="path in which to write the output")

    args = parser.parse_args()

    # load the corpus alignments
    wrd_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tdev2'),
            'tdev2/share/{}.wrd'.format(args.corpus))
    phn_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tdev2'),
            'tdev2/share/{}.phn'.format(args.corpus))
 
    print('Reading gold')
    gold = Gold(wrd_path=wrd_path, 
                phn_path=phn_path)

    print('Reading discovered classes')
    disc = Disc(args.disc_clsfile, gold) 

    measures = args.measures
    output = args.output

    # Launch evaluation of each metric and write it 
    # in the output
    if len(measures) == 0 or "boundary" in measures:
        print('Computing Boundary...')
        boundary = Boundary(gold, disc, output)
        boundary.compute_boundary()
        boundary.write_score()
    if len(measures) == 0 or "grouping" in measures:
        print('Computing Grouping...')
        grouping = Grouping(disc, output, args.njobs)
        grouping.compute_grouping()
        grouping.write_score()
    if len(measures) == 0 or "token/type" in measures:
        print('Computing Token and Type...')
        token_type = TokenType(gold, disc, output)
        token_type.compute_token_type()
        token_type.write_score()
    if len(measures) == 0 or "coverage" in measures:
        print('Computing Coverage...')
        coverage = Coverage(gold, disc, output)
        coverage.compute_coverage()
        coverage.write_score()
    if len(measures) == 0 or "ned" in measures:
        print('Computing NED...')
        ned = Ned(disc, output)
        ned.compute_ned()
        ned.write_score()

    
if __name__ == "__main__": 
    main()
