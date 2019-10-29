#!/usr/bin/python

# Load packages.
import math, numpy as np, scipy as sp, scipy.stats
import os, sys, argparse

from common import em, log_likelihood_ratio, load_node_score, save_node_score, load_nodes

# Parse arguments.
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Input score file')
    parser.add_argument('-p', '--p_values', action='store_true', help='Transform p-values')
    parser.add_argument('-t', '--threshold', action='store_true', help='Use mixing model for threshold')
    parser.add_argument('-onf', '--outlier_node_file', type=str, required=False, help='Outlier node file')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Output score file')
    return parser

# Run script.
def run(args):
    # Load data.
    node_to_score = load_node_score(args.input_file)

    nodes = sorted(node_to_score)
    scores = np.array([node_to_score[node] for node in nodes])

    # Optionally transform p-values to z-scores, i.e., z = \Phi^{-1}(1 - p).
    if args.p_values:
        scores = sp.stats.norm.isf(scores)

    # Estimate mixture model parameters; optionally remove potential outlier nodes from fit.
    if args.outlier_node_file is None:
        mu, pi = em(scores)
    else:
        outlier_nodes = load_nodes(args.outlier_node_file)
        non_outlier_nodes = sorted(set(nodes)-set(outlier_nodes))
        non_outlier_scores = np.array([node_to_score[node] for node in non_outlier_nodes])
        mu, pi = em(non_outlier_scores)

    # Convert scores to log-likelihood ratios.
    scores = log_likelihood_ratio(scores, mu, pi)

    # Optionally shift scores to threshold giving by mixture model parameters.
    if args.threshold:
        if args.outlier_node_file is None:
            n = np.size(scores)
            k = int(round(pi*n))
            sorted_scores = np.sort(scores)[::-1]
            threshold = 0.5*(sorted_scores[max(0, k-1)] + sorted_scores[min(k, n-1)])
            scores -= threshold
        else:
            n = np.size(scores)
            k = int(round(pi*n)) + len(outlier_nodes)
            sorted_scores = np.sort(scores)[::-1]
            threshold = 0.5*(sorted_scores[max(0, k-1)] + sorted_scores[min(k, n-1)])
            scores -= threshold

    # Save results.
    node_to_score = dict(zip(nodes, scores))
    save_node_score(args.output_file, node_to_score)

if __name__=='__main__':
    run(get_parser().parse_args(sys.argv[1:]))
