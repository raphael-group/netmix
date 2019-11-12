#!/usr/bin/python

import math, numpy as np, scipy as sp, scipy.stats

################################################################################
#
# Gaussian mixture model functions
#
################################################################################

# Define functions.
def pdf(x, mu=0.0, sigma=1.0):
    return sp.stats.norm.pdf(x, mu, sigma)

def cdf(x, mu=0.0, sigma=1.0):
    return sp.stats.norm.cdf(x, mu, sigma)

def sf(x, mu=0.0, sigma=1.0):
    return sp.stats.norm.sf(x, mu, sigma)

def likelihood_ratio(x, mu, alpha):
    a = alpha*pdf(x, mu)
    b = (1-alpha)*pdf(x)
    return b/a

def log_likelihood_ratio(x, mu, alpha):
    a = alpha*pdf(x, mu)
    b = (1-alpha)*pdf(x)
    return np.log(a)-np.log(b)

def log_likelihood_sum(x, mu, alpha):
    a = alpha*pdf(x, mu)
    b = (1-alpha)*pdf(x)
    return np.nansum(np.log(a+b))

def responsibility(x, mu, alpha):
    a = alpha*pdf(x, mu)
    b = (1-alpha)*pdf(x)
    return a/(a+b)

def log_responsibility(x, mu, alpha):
    a = alpha*pdf(x, mu)
    b = (1-alpha)*pdf(x)
    return np.log(a)-np.log(a+b)

def single_em(x, mu=0.0, alpha=0.5, tol=1e-3, max_num_iter=10**3):
    x = np.asarray(x)
    a = np.zeros(np.shape(x))
    b = np.zeros(np.shape(x))
    gamma = np.zeros(np.shape(x))
    n = np.size(x)

    previous_log_likelihood = log_likelihood_sum(x, mu, alpha)

    for _ in range(max_num_iter):
        # Perform E step.
        a[:] = alpha*pdf(x, mu)
        b[:] = (1-alpha)*pdf(x)
        gamma[:] = a/(a+b)

        # Perform M step.
        sum_gamma = np.sum(gamma)
        mu = np.sum(gamma*x)/sum_gamma
        alpha = sum_gamma/n

        # Check for convergence.
        current_log_likelihood = log_likelihood_sum(x, mu, alpha)
        if current_log_likelihood<(1+tol)*previous_log_likelihood:
            break
        else:
            previous_log_likelihood = current_log_likelihood

    return mu, alpha

def em(x, tol=1e-3, max_num_iter=10**3, num_trials=10):
    x = np.sort(np.asarray(x).flatten())[::-1]
    n = np.size(x)

    mus = np.zeros(num_trials)
    alphas = np.zeros(num_trials)
    log_likelihoods = np.zeros(num_trials)

    # Initialize EM algorithm by partitioning scores into high and low
    # components and using size and sample mean of higher component as
    # estimates of size and distribution mean of altered subnetwork.
    for trial in range(num_trials):
        alpha = (trial+0.5)/num_trials
        k = int(round(alpha*n))
        mu = np.mean(x[:k]) if k>0 else 0.0

        mu, alpha = single_em(x, mu, alpha, tol, max_num_iter)

        mus[trial] = mu
        alphas[trial] = alpha
        log_likelihoods[trial] = log_likelihood_sum(x, mu, alpha)

    trial = np.argmax(log_likelihoods)
    return mus[trial], alphas[trial]

################################################################################
#
# Other mathematical functions
#
################################################################################

def compute_jaccard_index(x, y):
    if len(x)>0 or len(y)>0:
        x, y = set(x), set(y)
        return float(len(x & y))/float(len(x | y))
    else:
        return float('nan')

def compute_recall_precision(positive, true):
    positive = set(positive)
    true = set(true)
    true_positive = true & positive

    num_positive = len(positive)
    num_true = len(true)
    num_true_positive = len(true_positive)

    if num_positive and num_true:
        recall = float(num_true_positive)/float(num_true)
        precision = float(num_true_positive)/float(num_positive)
    else:
        recall = float('nan')
        precision = float('nan')

    return recall, precision

def compute_recall(positive, true):
    recall, _ = compute_recall_precision(positive, true)
    return recall

def compute_precision(positive, true):
    _, precision = compute_recall_precision(positive, true)
    return precision

def compute_f_measure(positive, true):
    recall, precision = compute_recall_precision(positive, true)
    if not math.isnan(recall) and not math.isnan(precision) and recall+precision:
        return 2.0*(recall*precision)/(recall+precision)
    else:
        return float('nan')

def compute_fdr(positive, true):
    positive = set(positive)
    true = set(true)
    false_positive = positive - true

    num_positive = len(positive)
    num_false_positive = len(false_positive)

    if num_positive:
        return float(num_false_positive)/float(num_positive)
    else:
        return float('nan')

################################################################################
#
# IO functions
#
################################################################################

def is_number(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def load_nodes(filename):
    '''
    Load nodes.
    '''
    nodes = set()
    with open(filename, 'r') as f:
        for l in f:
            if not l.startswith('#'):
                arrs = l.rstrip().split()
                nodes |= set(arrs)
    return nodes

def save_nodes(filename, nodes):
    '''
    Load nodes.
    '''
    with open(filename, 'w') as f:
        f.write('\n'.join(str(node) for node in nodes))

def load_node_score(filename):
    '''
    Load node scores.
    '''
    node_to_score = dict()
    with open(filename, 'r') as f:
        for l in f:
            if not l.startswith('#'):
                arrs = l.strip().split()
                if len(arrs)==2:
                    node = arrs[0]
                    if is_number(arrs[1]):
                        score = float(arrs[1])
                        if np.isfinite(score):
                            node_to_score[node] = score
                    else:
                        raise Warning('{} is not a valid node score; input line omitted.'.format(l.strip()))
                elif arrs:
                    raise Warning('{} is not a valid node score; input line omitted.'.format(l.strip()))

    if not node_to_score:
        raise Exception('No node scores; check {}.'.format(filename))

    return node_to_score

def save_node_score(filename, node_to_score, reverse=True):
    '''
    Save node scores.
    '''
    node_score_list = sorted(node_to_score.items(), key=lambda node_score: (-float(node_score[1]) if reverse else float(node_score[1]), node_score[0]))
    with open(filename, 'w') as f:
        f.write('\n'.join('{}\t{}'.format(node, score) for node, score in node_score_list))

def load_edge_list(filename):
    '''
    Load edge list.
    '''
    edge_list = list()
    with open(filename, 'r') as f:
        for l in f:
            if not l.startswith('#'):
                arrs = l.strip().split()
                if len(arrs)>=2:
                    u, v = arrs[:2]
                    edge_list.append((u, v))
                elif arrs:
                    raise Warning('{} is not a valid edge; input line omitted.'.format(l.strip()))

    if not edge_list:
        raise Exception('Edge list has no edges; check {}.'.format(filename))

    return edge_list

def save_edge_list(filename, edge_list):
    '''
    Save edge list.
    '''

    with open(filename, 'w') as f:
        f.write('\n'.join('\t'.join(map(str, edge)) for edge in edge_list))

def load_matrix(filename, matrix_name='A', dtype=np.float32):
    '''
    Load matrix.
    '''
    import h5py

    f = h5py.File(filename, 'r')
    if matrix_name in f:
        A = np.asarray(f[matrix_name].value, dtype=dtype)
    else:
        raise KeyError('Matrix {} is not in {}.'.format(matrix_name, filename))
    f.close()
    return A

def save_matrix(filename, A, matrix_name='A', dtype=np.float32):
    '''
    Save matrix.
    '''
    import h5py

    f = h5py.File(filename, 'a')
    if matrix_name in f:
        del f[matrix_name]
    f[matrix_name] = np.asarray(A, dtype=dtype)
    f.close()

def status(message=''):
    '''
    Write status message to screen; overwrite previous status message and do not
    advance line.
    '''
    import sys

    try:
        length = status.length
    except AttributeError:
        length = 0

    sys.stdout.write('\r'+' '*length + '\r'+str(message))
    sys.stdout.flush()
    status.length = max(len(str(message).expandtabs()), length)
