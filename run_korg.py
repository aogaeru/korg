#!/usr/bin/env python
# vim: tabstop=4:softtabstop=4:shiftwidth=4:expandtab:

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from korg import LineGrokker, PatternRepo

if __name__ == '__main__':
    descr = "Tests a pattern on a log source"
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, description=descr)
    parser.add_argument('-p', '--patterns', dest='patterns', nargs='+',
        metavar='DIR', help='space-separated list of paths to supplemental pattern directories')
    parser.add_argument('-l', '--logfile', dest='logfile',  default='/dev/stdin',
        metavar='FILE', help='logfile to process')
    parser.add_argument('-g', '--grokker', dest='grokker',  default='%{SYSLOGBASE}',
        metavar='PATTERN', help='pattern to test')
    parser.add_argument('-f', '--fields', dest='fields', default=None, nargs='+',
        metavar='FIELD', help='restrict output to specified fields')
    parser.add_argument('-v', '--verbose', dest='verbose', default=False,
        action='store_true', help='enable verbose output')
    parser.add_argument('-a', '--all', dest='allprint', default=False,
        action='store_true', help='print non-matching lines too')
    args = parser.parse_args()

    if args.logfile == '-':
        args.logfile = '/dev/stdin'

    # load the pattern map
    pr = PatternRepo(args.patterns)
    lg = LineGrokker(args.grokker, pr)

    with open(args.logfile) as infile:
        for line in infile:
            grokked = lg.grok(line)
            if args.verbose:
                print "=============================="
                print line.strip()
            if grokked is None and args.allprint is False:
                continue
            if args.fields:
                print dict([(key, grokked.get(key, None)) for key in args.fields])
            else:
                print grokked
