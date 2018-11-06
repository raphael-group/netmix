#!/usr/bin/python

# Load packages.
import math, numpy as np, scipy as sp, scipy.stats, networkx as nx
import os, sys, argparse

from common import load_node_score, load_edge_list

# Parse arguments.
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Score file')
    parser.add_argument('-elf', '--edge_list_file', type=str, required=False, help='Edge list file')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Subset file')
    return parser

# Run script.
def run(args):
    node_to_score = load_node_score(args.input_file)
    positive_nodes = set(node for node, score in node_to_score.items() if score>0)

    if args.edge_list_file is not None:
        edge_list = load_edge_list(args.edge_list_file)
        G = nx.Graph()
        G.add_edges_from(edge_list)
        G = G.subgraph(positive_nodes)
        nonsingleton_components = [set(component) for component in nx.connected_components(G) if len(component)>1]
        if nonsingleton_components:
            positive_nodes = set.union(*nonsingleton_components)
        else:
            positive_nodes = set()

    positive_nodes = sorted(positive_nodes, key=lambda node: -node_to_score[node])
    with open(args.output_file, 'w') as f:
        f.write('\n'.join(positive_nodes))

if __name__=='__main__':
    run(get_parser().parse_args(sys.argv[1:]))
