#!/usr/bin/env bash

################################################################################
#
#   Instructions
#
################################################################################

# Run NetMix by running
#
#    ./netmix.sh network.tsv scores.tsv output.txt
#
# where network.tsv is a tab-delimited edge list and scores.tsv is a tab-
# delimited list of p-values on the nodes of network.tsv. The README provides
# more complete instructions for use.

################################################################################
#
#   Set environment and parameters.
#
################################################################################

network="$1"
scores="$2"
output="$3"

netmix_directory=src
heinz_directory=""
tmp_directory=tmp

if [ $heinz_directory=="" ]
then
    echo "Error: heinz directory not provided; install heinz and set the heinz directory in this file to use NetMix."
    exit
fi

if [ ! -f $heinz_directory/heinz ]
then
    echo "Error: \""$heinz"/heinz\" does not exist; install heinz and set the heinz directory in this file to use NetMix."
    exit
fi

mkdir -p $tmp_directory

num_cores=4 # Number of cores
max_num_seconds=1800 # Maximum number of seconds

################################################################################
#
#   Find altered subnetwork.
#
################################################################################

# Generate responsibility scores for p-values.
python $netmix_directory/compute_scores.py \
    -i $scores \
    -o $tmp_directory/responsibility_scores.tsv

# Run heinz on responsibility scores.
$heinz_directory/./heinz \
    -e $network \
    -n $tmp_directory/responsibility_scores.tsv \
    -o $tmp_directory/heinz_output.tsv \
    -m $num_cores \
    -t $max_num_scores \
    -v 0 \
    > /dev/null 2>&1

# Parse heinz output.
python $netmix_directory/process_heinz_output.py \
    -i $tmp_directory/heinz_output.tsv \
    -o $output

# Remote temporary files.
rm -f $tmp_directory/responsibility_scores.tsv $tmp_directory/heinz_output.tsv
