import sys
import time
import argparse
from progress import Progress
import random


def load_graph(args):
    """Load graph from text file

    Parameters:
    args -- arguments named tuple

    Returns:
    A dict mapling a URL (str) to a list of target URLs (str).
    """
    g = dict()
    # Iterate through the file line by line
    for line in args.datafile:
        # And split each line into two URLs
        node, target = line.split()
        list = []
        append = list.append
        if node not in g:
            append(target)
            g[node] = list
        else:
            g[node].append(target)
    return g


def print_stats(graph):
    """Print number of nodes and edges in the given graph"""
    e_count = 0
    # count number of nodes
    n_count = len(graph)
    # count number of edges
    for node in graph:
        e_count += len(graph[node])
    print("number of nodes:", n_count, "number of edges:", e_count)


def stochastic_page_rank(graph, args):
    """Stochastic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its hit frequency

    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """

    n_repetitions = args.repeats
    n_steps = args.steps
    # initialize hit_count[node] with 0 for all nodes
    hit_count = {node: 0 for node in graph}

    # repeat n_repetitions times:
    for j in range(n_repetitions):
        # current_node <- randomly selected node
        current_node = random.choice(list(graph))
        # repeat n_steps times:
        for i in range(n_steps):
            # current_node <- uniformly randomly chosen among the out edges of current_node
            current_node = random.choice(graph[current_node])
            if current_node not in graph:
                break
        # hit_count[current_node] += 1 / n_repetitions
        hit_count[current_node] += 1 / n_repetitions
    return hit_count




def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.

    """
    n_steps = args.steps
    # initialize node_prob[node] = 1/(number of nodes) for all nodes
    node_prob = {node: 1 / len(graph) for node in graph}

    # repeat n_steps times:
    for i in range(n_steps):
        #  initialize next_prob[node] = 0 for all nodes
        next_prob = {node: 0 for node in graph}
        # for each node:
        for node in graph:
            # p <- node_prob[node] divided by its out degree
            p = node_prob[node] / (len(graph[node]))
            # for each target among out edges of node:
            for target in graph[node]:
                # next_prob[target] += p
                next_prob[target] += p
        # node_prob <- next_prob
        node_prob = next_prob
    # return
    return node_prob




parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")


if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")
