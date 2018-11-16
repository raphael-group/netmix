#!/usr/bin/env bash

scripts=../src
data=data
results=results
heinz_directory=""  # Install heinz and add the directory for heinz here.

if [ ! -f $heinz_directory/heinz ]
then
    echo "\""$heinz"/heinz\" does not exist; install to identify NSGMM."
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
pi=0.02     # Fraction of nodes drawn from altered distribution
seed=12345  # Random seed

mkdir -p $data
mkdir -p $results

# Generate random network.
python $scripts/generate_barabasi_albert_graph.py \
    -n   $n \
    -m   $m \
    -s   $seed \
    -elf $data/network.tsv

# Generate random scores.
python $scripts/generate_weights.py \
    -elf $data/network.tsv \
    -mu  $mu \
    -pi  $pi \
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

# Generate likelihood-based scores.
python $scripts/generate_llr_scores.py \
    -i $data/z_scores.tsv \
    -o $data/llr_scores.tsv

# Find nodes for GMM problem.
python $scripts/find_maximum_subset.py \
    -i $data/llr_scores.tsv \
    -o $results/gmm_results.txt

# Find nodes for NSGMM problem.
if [ -f $heinz_directory/heinz ]
then
    $heinz_directory/./heinz \
        -e $data/network.tsv \
        -n $data/llr_scores.tsv \
        -o $results/nsgmm_output.tsv \
        -m 4 \
        -t 1800 \
        -v 0 \
        > /dev/null 2>&1
fi

python $scripts/process_heinz_output.py \
    -i $results/nsgmm_output.tsv \
    -o $results/nsgmm_results.txt
    
rm -f $results/nsgmm_output.tsv
