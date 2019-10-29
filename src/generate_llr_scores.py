#!/usr/bin/python

# Load packages.
import math, numpy as np, scipy as sp, scipy.stats
import os, sys, argparse

from common import em, log_likelihood_ratio, load_node_score, save_node_score, load_nodes

# Parse arguments.
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Observed score file')
    parser.add_argument('-p', '--p_values', action='store_true', help='Transform p-values')
    parser.add_argument('-onf', '--outlier_node_file', type=str, required=False, help='Outlier node file')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Likelihood score file')
    return parser

# Run script.
def run(args):
    # Load data.
    node_to_score = load_node_score(args.input_file)

    nodes = sorted(node_to_score)
    scores = np.array([node_to_score[node] for node in nodes])
    n = len(scores)

    # Transform p-values to z-scores, i.e., z = \Phi^{-1}(1 - p).
    if args.p_values:
        scores = sp.stats.norm.isf(scores)

    # Estimate mixture model parameters; remove potential outlier nodes from fit.
    if args.outlier_node_file is None:
        mu, pi = em(scores)
    else:
        outlier_nodes = load_nodes(args.outlier_node_file)
        non_outlier_nodes = sorted(set(nodes)-set(outlier_nodes))
        non_outlier_scores = np.array([node_to_score[node] for node in non_outlier_nodes])
        mu, pi = em(non_outlier_scores)

    # Convert scores to log-likelihood ratios.
    scores = log_likelihood_ratio(scores, mu, pi)

    # Save results.
    node_to_score = dict(zip(nodes, scores))
    save_node_score(args.output_file, node_to_score)

if __name__=='__main__':
    run(get_parser().parse_args(sys.argv[1:]))
