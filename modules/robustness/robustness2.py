#!/usr/bin/python
# Author: Hernán David Carvajal <carvajal.hernandavid at gmail.com>
# Tested in python-3.4.3


import sys
import operator
import random as rnd
import networkit as nk
import networkx as nx


def random(g):
    nodes = g.nodes()
    random.shuffle(nodes)

    return nodes


def degree_centrality(g):
    degrees = nx.degree_centrality(g)
    ordered = sorted(degrees.items(), key=operator.itemgetter(1), reverse=True)

    return [x[1] for x in ordered]


def betweenness_centrality(g):
    results = nx.degree_centrality(g)
    ordered = sorted(results.items(), key=operator.itemgetter(1), reverse=True)

    return [x[1] for x in ordered]


def eigenvector_centrality(g):
    results = nx.eigenvector_centrality(g)
    ordered = sorted(results.items(), key=operator.itemgetter(1), reverse=True)

    return [x[1] for x in ordered]


def calculate_robustness(g):
    largest_component_size = sorted(nx.connected_components(g), key = len, reverse=True)
    n = len(g.nodes())

    return largest_component_size / n


def robustness_index(g, sequential=True):
    n = len(g.nodes())
    r = 0.0
    rank = ranking(g)

    for i in range(1, n):
        g.remove_node(next(rank))
        r += calculate_robustness(g)

        if not sequential:
            rank = ranking(g)

    return 0.5 - (r / n)


def ranking(g, strategy=""):
    return []

def main(argv):
    None

if __name__ == "__main__":
    main(sys.argv[1:])
