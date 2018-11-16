#!/usr/bin/python

# Load packages.
import math
import os, sys, argparse

# Parse arguments.
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, required=True)
    parser.add_argument('-o', '--output_file', type=str, required=True)
    return parser

# Define functions.
def load_heinz_results(filename):
    node_to_score = dict()
    try:
        with open(filename, 'r') as f:
            for l in f:
                if not l.startswith('#'):
                    arrs = l.rstrip('\n').split('\t')
                    if len(arrs)==2:
                        node = arrs[0]
                        score = arrs[1]
                        if score!='NaN':
                            node_to_score[node] = float(score)
    except:
        pass
    return sorted(node_to_score, key=lambda node: (-node_to_score[node], node))

# Run script.
def run(args):
    heinz_results = load_heinz_results(args.input_file)

    with open(args.output_file, 'w') as f:
        f.write('\n'.join(sorted(heinz_results)))

if __name__=='__main__':
    run(get_parser().parse_args(sys.argv[1:]))
