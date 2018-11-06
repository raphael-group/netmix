#!/usr/bin/python

# Load modules.
import sys, argparse

from common import load_node_score

# Parse arguments.
def get_parser():
    description = 'Evaluate statistical significance.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-osf', '--observed_score_file', type=str, required=True, help='Observed score file')
    parser.add_argument('-orf', '--observed_results_file', type=str, required=True, help='Observed results file')
    parser.add_argument('-psf', '--permuted_score_files', type=str, required=True, nargs='*', help='Permuted score files')
    parser.add_argument('-prf', '--permuted_results_files', type=str, required=True, nargs='*', help='Permuted results files')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Output file')
    return parser

# Run script.
def run(args):
    # Find observed subnetwork score.
    observed_node_to_score = load_node_score(args.observed_score_file)
    observed_results = load_nodes(args.observed_results_file)
    observed_subnetwork_score = sum(observed_node_to_score[node] for node in observed_results)

    # Find permuted subnetwork scores.
    permuted_subnetwork_scores = list()
    for permuted_score_file, permuted_results_file in zip(args.permuted_score_files, args.permuted_score_files):
        permuted_node_to_score = load_node_score(args.permuted_score_file)
        permuted_results = load_nodes(args.permuted_results_file)
        permuted_subnetwork_score = sum(permuted_node_to_score[node] for node in permuted_results)
        permuted_subnetwork_scores.append(permuted_subnetwork_score)

    # Compute subnetwok scores.
    expected_subnetwork_score = np.mean(permuted_subnetwork_scores)

    # Compare results.
    num_extreme_permuted_scores = sum(1 for permuted_subnetwork_score in permuted_subnetwork_scores if permuted_subnetwork_score>=observed_subnetwork_score)
    num_total_permuted_scores = len(permuted_subnetwork_scores)
    p_value = float(num_extreme_permuted_scores)/float(num_total_permuted_scores)

    output_string = 'Observed subnetwork score: {}\nExpected subnetwork score: {}\np-value: {}'.format(observed_subnetwork_score, expected_subnetwork_score, p_value)
    with open(args.output_file, 'w') as f:
        f.write(output_string)

if __name__=='__main__':
    run(get_parser().parse_args(sys.argv[1:]))
