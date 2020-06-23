NetMix
=======================

NetMix is an algorithm for identifying altered subnetworks with node scores that are distributed differently from other nodes in the network. NetMix improves upon current methods by using a Gaussian Mixture Model to find a less biased estimate of the size of an altered subnetwork. *This README is under construction.*

Setup
------------------------
The setup process for NetMix requires the following steps:

### Download
Download NetMix. The following command clones the current NetMix repository from GitHub:

    git clone https://github.com/raphael-group/netmix.git

### Installation

##### Required

* Linux/Unix
* [Python (2.7 or 3.6)](http://python.org/)
* [NumPy (1.17)](http://www.numpy.org/)
* [SciPy (1.3)](http://www.scipy.org/)
* [h5py (2.10)](http://www.h5py.org/)
* [heinz](https://github.com/ls-cwi/heinz)

##### Optional

* [Virtualenv (for Python 2)](https://virtualenv.pypa.io/)
* [Virtualenv (for Python 3)](https://docs.python.org/3/library/venv.html)
* [NetworkX (2.4)](http://networkx.github.io/)

Most likely, NetMix will work with other versions of the above software. We recommend using a Python virtual environment, which allows Python packages to be installed or updated independently of system packages. The [heinz](https://github.com/ls-cwi/heinz) package **must** be installed before using NetMix. You can set the location for heinz in the `netmix.sh` script.

### Use

To test NetMix on example data, please run the following command:

    ./netmix.sh network.tsv scores.tsv output.txt

where `network.tsv` is a tab-delimited edge list and `scores.tsv` is a tab-delimited list of *p*-values on the nodes of `network.tsv`. Please see below for more details.

----------------
NetMix has three main steps:
1. Compute node scores.
2. Find the maximum-weight connected subgraph using the node scores.
3. (Optional) Compute statistical significance.

The NetMix [manuscript](https://link.springer.com/chapter/10.1007%2F978-3-030-45257-5_11) defines these steps, and the NetMix [script](https://github.com/raphael-group/netmix/blob/master/netwmixs.sh) combines them. To compute permuted networks and scores for evaluating statistical signficance, see the Hierarchical HotNet [paper](https://academic.oup.com/bioinformatics/article/34/17/i972/5093236) and [repository](https://github.com/raphael-group/hierarchical-hotnet), which describes and implements multiple [network](https://github.com/raphael-group/hierarchical-hotnet/blob/master/src/permute_network.py) and [score](https://github.com/raphael-group/hierarchical-hotnet/blob/master/src/permute_scores.py) permutation schemes.

These steps take the following inputs and return the following output.

### Input
NetMix has two input files that together define a network with scores on the nodes of the network. For example, the following example defines a network with nodes `A`, `B`, and `C`, where `C` is directly connected to both `A` and `B` and `A`, `B`, and `C` have *p*-values of `0.1`, `0.5`, and `0.9`, respectively.

##### Edge list file
Each edge in this file corresponds to an edge in the network.

    A    C
    B    C

##### Gene-to-score file
Each line in this file associates a node with a score:

    A    0.1
    B    0.5
    C    0.9

### Output
NetMix reports a set of nodes corresponding to the maximum-weight connected subgraph (MWCS) for our node scores. For example, the MWCS includes nodes `B` and `C` but not node `A`. Each line in the output file is a node:

    B
    C

Additional information
----------------

### Examples
See the `examples` directory for an example that should complete in a few minutes on most machines.

### Support
If you are unable to run the example in the `examples` directory, then please post an issue on GitHub.

### License
See `LICENSE` for license information.

### Citation
If you use NetMix in your work, then please cite the following [manuscript](https://link.springer.com/chapter/10.1007%2F978-3-030-45257-5_11).

> M.A. Reyna*, U. Chitra*, R. Elyanow, B.J. Raphael. NetMix: A network-structured mixture model for reducing bias in the identification of altered subnetworks. RECOMB 2020.
