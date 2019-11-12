#!/usr/bin/python

# Load packages.
import numpy as np, networkx as nx
import sys, argparse

from common import load_node_score, load_edge_list, save_nodes

# Parse arguments.
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Score file')
    parser.add_argument('-k', type=int, required=False, help='Set size')
    parser.add_argument('-elf', '--edge_list_file', type=str, required=False, help='Edge list file')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Set file')
    return parser

# Run script.
def run(args):
    node_to_score = load_node_score(args.input_file)

    nodes = sorted(node_to_score)
    scores = np.asarray([node_to_score[node] for node in nodes])
    indices = np.argsort(scores)[::-1]
    n = len(nodes)

    set_scores = np.cumsum(scores[indices])/np.sqrt(np.arange(1, n+1))
    set_size = np.argmax(set_scores)+1 if set_scores[0]>0 else 0
    set_nodes = [nodes[i] for i in indices[:set_size]]

    if args.edge_list_file is not None:
        edge_list = load_edge_list(args.edge_list_file)

        G = nx.Graph()
        G.add_edges_from(edge_list)
        G = G.subgraph(set_nodes)

        nonsingleton_components = [set(component) for component in nx.connected_components(G) if len(component)>1]
        if nonsingleton_components:
            set_nodes = set.union(*nonsingleton_components)
        else:
            set_nodes = set()

    sorted_nodes = sorted(set_nodes, key=lambda node: -node_to_score[node])
    save_nodes(args.output_file, sorted_nodes)

if __name__=='__main__':
    run(get_parser().parse_args(sys.argv[1:]))
