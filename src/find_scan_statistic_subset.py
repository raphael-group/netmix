#!/usr/bin/python

# Load packages.
import math, numpy as np, scipy as sp, scipy.stats, networkx as nx
import os, sys, argparse

from common import load_node_score, load_edge_list

# Parse arguments.
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, required=True)
    parser.add_argument('-k', type=int, required=False)
    parser.add_argument('-elf', '--edge_list_file', type=str, required=False)
    parser.add_argument('-cof', '--check_output_file', action='store_true')
    parser.add_argument('-o', '--output_file', type=str, required=True)
    return parser

# Run script.
def run(args):
    if args.check_output_file and os.path.isfile(args.output_file):
        sys.exit()

    node_to_score = load_node_score(args.input_file)

    nodes = sorted(node_to_score)
    scores = np.asarray([node_to_score[node] for node in nodes])
    indices = np.argsort(scores)[::-1]
    n = len(nodes)

    set_scores = np.cumsum(scores[indices])/np.sqrt(np.arange(1, n+1))
    set_size = np.argmax(set_scores)+1 if np.max(set_scores)>0 else 0
    set_nodes = [nodes[i] for i in indices[:set_size]]

    if args.edge_list_file is not None:
        edge_list = load_edge_list(args.edge_list_file)
        G = nx.Graph()
        G.add_edges_from(edge_list)
        G = G.subgraph(set_nodes)
        set_nodes = set.union(*(set(component) for component in nx.connected_components(G) if len(component)>1))

    set_nodes = sorted(set_nodes, key=lambda node: -node_to_score[node])
    with open(args.output_file, 'w') as f:
        f.write('\n'.join(set_nodes))

if __name__=='__main__':
    run(get_parser().parse_args(sys.argv[1:]))
