#!/usr/bin/env bash

################################################################################
#
#   Set directories.
#
################################################################################

scripts=../src
data=data
results=results
heinz_directory=""  # Install heinz and add the directory for heinz here.

mkdir -p $data
mkdir -p $results

if [ ! -f $heinz_directory/heinz ]
then
    echo "\""$heinz"/heinz\" does not exist; install to use NetMix."
fi

################################################################################
#
#   Generate simulated data.
#
################################################################################

echo "Generating simulated data..."

n=1000      # Number of nodes
m=5         # Parameter for Barabasi-Albert preferential attachment model
mu=2.5      # Altered distribution mean
alpha=0.02  # Fraction of nodes drawn from altered distribution
seed=12345  # Random seed

# Generate random network.
python $scripts/generate_barabasi_albert_graph.py \
    -n   $n \
    -m   $m \
    -s   $seed \
    -elf $data/network.tsv

# Generate random scores.
python $scripts/generate_vertex_weights.py \
    -elf $data/network.tsv \
    -mu  $mu \
    -a   $alpha \
    -is  $seed \
    -ss  $seed \
    -nsf $data/z_scores.tsv \
    -inf $data/implanted_nodes.tsv \
    -nnf $data/non_implanted_nodes.tsv

################################################################################
#
#   Identify altered subnetwork.
#
################################################################################

echo "Identifying altered subnetwork..."

# Generate responsibility-based scores.
python $scripts/compute_scores.py \
    -i $data/z_scores.tsv \
    -o $data/responsibility_scores.tsv

# Find nodes for unconstrained ASD problem.
python $scripts/compute_positive_subset.py \
    -i $data/responsibility_scores.tsv \
    -o $results/asd_unconstrained_results.txt

# Find nodes for constrained ASD problem.
if [ -f $heinz_directory/heinz ]
then
    $heinz_directory/./heinz \
        -e $data/network.tsv \
        -n $data/responsibility_scores.tsv \
        -o $results/asd_constrained_output.tsv \
        -m 4 \
        -t 1800 \
        -v 0 \
        > /dev/null 2>&1
fi

python $scripts/process_heinz_output.py \
    -i $results/asd_constrained_output.tsv \
    -o $results/asd_constrained_results.txt

rm -f $results/asd_constrained_output.tsv
