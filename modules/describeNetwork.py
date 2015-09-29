#!/usr/bin/python

"""
This script performs a basic analysis on the given network, measuring some
features like the number of nodes, number of links, the average path length and
the average clustering coefficient.

Usage: python describeNetwork.py <infile>

where infile is the name of the network file in gml format.
"""

import sys
import networkx as nx


def main(argv):
    """
    Entry point
    """

    infile = argv[0]
    g = nx.read_gml(infile)

    print("Number of nodes: {}".format(nx.number_of_nodes(g)))
    print("Number of links: {}".format(nx.number_of_edges(g)))
    print("Average path length: {}".format(nx.average_shortest_path_length(g)))
    print("Clustering coefficient: {}".format(nx.average_clustering(g)))

if __name__ == "__main__":
    main(sys.argv[1:])
