#!/usr/bin/python

# Load packages.
import math, numpy as np, scipy as sp, scipy.stats, random, networkx as nx
import sys, argparse

from common import load_edge_list, save_edge_list, save_node_score

# Parse arguments.
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-elf', '--edge_list_file', type=str, required=True)
    parser.add_argument('-mu', type=float, required=True)
    parser.add_argument('-pi', type=float, required=True)
    parser.add_argument('-is', '--implant_seed', type=int, required=False)
    parser.add_argument('-ss', '--score_seed', type=int, required=False)
    parser.add_argument('-nsf', '--node_score_file', type=str, required=True)
    parser.add_argument('-inf', '--implanted_nodes_file', type=str, required=True)
    parser.add_argument('-nnf', '--non_implanted_nodes_file', type=str, required=True)
    return parser

# Run script.
def run(args):
    # Load network.
    edge_list = load_edge_list(args.edge_list_file)

    G = nx.Graph()
    G.add_edges_from(edge_list)

    nodes = set(G.nodes())
    sorted_nodes = sorted(G.nodes())
    num_nodes = G.number_of_nodes()

    assert 0<=args.pi<=1
    k = int(round(args.pi*num_nodes))

    # Choose implant.
    random.seed(args.implant_seed)

    # Traverse k distinct nodes with random walk on graph.
    implanted_nodes = set()
    if k>0:
        u = random.choice(sorted_nodes)
        implanted_nodes.add(u)
        while len(implanted_nodes)<k:
            neighbors = sorted(G.neighbors(u))
            u = random.choice(neighbors)
            implanted_nodes.add(u)
    non_implanted_nodes = nodes - implanted_nodes

    # Choose scores.
    np.random.seed(args.score_seed)
    implanted_scores = np.random.randn(k) + args.mu
    non_implanted_scores = np.random.randn(num_nodes-k)

    assert len(implanted_nodes)==len(implanted_scores)
    assert len(non_implanted_nodes)==len(non_implanted_scores)

    # Save data.
    implanted_nodes = sorted(implanted_nodes)
    non_implanted_nodes = sorted(non_implanted_nodes)

    node_to_score = dict()
    for node, score in zip(implanted_nodes, implanted_scores):
        node_to_score[node] = score
    for node, score in zip(non_implanted_nodes, non_implanted_scores):
        node_to_score[node] = score

    implanted_nodes = sorted(implanted_nodes, key=lambda node: (-node_to_score[node], node)) if implanted_nodes else []
    with open(args.implanted_nodes_file, 'w') as f:
        f.write('\n'.join(implanted_nodes))

    non_implanted_nodes_string = sorted(non_implanted_nodes, key=lambda node: (-node_to_score[node], node)) if non_implanted_nodes else []
    with open(args.non_implanted_nodes_file, 'w') as f:
        f.write('\n'.join(non_implanted_nodes))

    save_node_score(args.node_score_file, node_to_score)
    
if __name__=='__main__':
    run(get_parser().parse_args(sys.argv[1:]))
