#!/usr/bin/python

# Load packages.
import networkx as nx
import sys, argparse

from common import save_edge_list

# Parse arguments.
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, required=True)
    parser.add_argument('-m', type=int, required=True)
    parser.add_argument('-s', '--seed', type=int, required=False)
    parser.add_argument('-elf', '--edge_list_file', type=str, required=True)
    return parser

# Run script.
def run(args):
    G = nx.barabasi_albert_graph(args.n, args.m, args.seed)

    assert G.number_of_nodes()==args.n and nx.is_connected(G)

    edges = [(i+1, j+1) for i, j in G.edges()]
    sorted_edges = sorted(sorted(edge) for edge in edges)
    save_edge_list(args.edge_list_file, sorted_edges)

if __name__=='__main__':
    run(get_parser().parse_args(sys.argv[1:]))
