#!/usr/bin/python

# Load packages.
import math, numpy as np, scipy as sp, scipy.stats
import os, sys, argparse

from common import em, responsibility, log_likelihood_ratio, load_node_score, save_node_score, load_nodes,save_subgraph_size

# Parse arguments.
def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Input score file')
    parser.add_argument('-p', '--p_values', action='store_true', help='Transform p-values to z-scores')
    parser.add_argument('-sc', '--score_choice', type=str, choices=['r', 'responsibility', 'responsibilities', 'llr', 'log_likelihood_ratio', 'log_likelihood_ratios', 'z', 'z-score', 'z-scores', 'z_score', 'z_scores'], default='responsibilities', help='Choose scores')
    parser.add_argument('-tc', '--threshold_choice', type=str, choices=['mixing_proportions', 'natural', 'none'], default='mixing_proportions', help='Choose score threshold')
    parser.add_argument('-onf', '--outlier_node_file', type=str, required=False, help='Outlier node file')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Output score file')
    parser.add_argument('-os', '--output_size_file', type=str, help='Output file for size of subgraph')
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
        mu, alpha = em(scores)
    else:
        outlier_node_set = load_nodes(args.outlier_node_file)
        non_outlier_node_set = set(nodes) - outlier_nodes
        non_outlier_nodes = sorted(nonoutlier_node_set)
        non_outlier_scores = np.array([node_to_score[node] for node in non_outlier_nodes])
        mu, alpha = em(non_outlier_scores)

    # Compute scores.
    if args.score_choice in ['r', 'responsibility', 'responsibilities']:
        scores = responsibility(scores, mu, alpha)
    elif args.score_choice in ['llr', 'log_likelihood_ratio', 'log_likelihood_ratios']:
        scores = log_likelihood_ratio(scores, mu, alpha)
    elif args.score_choice in ['z', 'z-score', 'z-scores', 'z_score', 'z_scores']:
        pass
    else:
        raise NotImplementedError('{} score not implemented'.format(score_choice))

    # Shift scores.
    if args.threshold_choice in ['mixing_proportion']:
        if args.outlier_node_file is None:
            n = np.size(scores)
            k = int(round(alpha*n))
            sorted_scores = np.sort(scores)[::-1]
            threshold = 0.5*(sorted_scores[max(0, k-1)] + sorted_scores[min(k, n-1)])
            scores -= threshold
        else:
            n = np.size(scores)
            k = int(round(alpha*n)) + len(outlier_nodes)
            sorted_scores = np.sort(scores)[::-1]
            threshold = 0.5*(sorted_scores[max(0, k-1)] + sorted_scores[min(k, n-1)])
            scores -= threshold
    elif args.threshold_choice in ['natural']:
        if args.score_choice in ['r', 'responsibility', 'responsibilities']:
            scores -= 0.5
        elif args.score_choice in ['llr', 'log_likelihood_ratio', 'log_likelihood_ratios', 'z', 'z-score', 'z-scores', 'z_score', 'z_scores']:
            pass
        else:
            raise NotImplementedError('{} score not implemented'.format(score_choice))
    elif args.threshold_choice in ['none']:
        pass # do nothing

    # Save results.
    node_to_score = dict(zip(nodes, scores))
    save_node_score(args.output_file, node_to_score)

    if args.output_size_file:
        subgraph_size = int(np.size(scores)*alpha)
        save_subgraph_size(args.output_size_file, subgraph_size)

if __name__=='__main__':
    run(get_parser().parse_args(sys.argv[1:]))
