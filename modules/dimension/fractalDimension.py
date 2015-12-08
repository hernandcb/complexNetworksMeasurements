#!/usr/bin/python
# Author: Hernán David Carvajal <carvajal.hernandavid at gmail.com>
# Tested in python-3.4.3

import sys
import os
import time
import math

import pyximport
pyximport.install()

from .boxCovering.greedyColoringC import *


def fractal_dimension(g, iterations=10000, debug=True):
    """
    This method computes the fractal dimension (D) of a network performing a box
    covering and analysing the relation between the minimum number of boxes (Nb)
    required to cover the graph and the dimension of each box (Lb).
    Then, given the relation:

                Nb ~ Lb raised to D

    To get the minimum number of boxes required to cover a graph given a box
    length, this method repeat the box covering several times (10.000 by
    default) and calculate the average value.

    Parameters
    ------------
    g: A networkit graph
    iterations: The number of times that the box covering algorithm will be run
    debug: If this variable is set to True the results of each iteration are
            saved into a file called results.csv

    Returns
    -----------
    A float value representing the fractal dimension of the network.
    """
    import networkit as nk
    import networkx as nx
    import numpy as np


    num_nodes =  g.numberOfNodes()
    # distances = all_pairs_shortest_path_length(g)
    gx = nk.nk2nx(g)
    distances = nx.shortest_paths.floyd_warshall_numpy(gx).astype(np.int)
    diameter = np.amax(distances)

    results = np.empty((iterations, diameter+1), dtype=int)

    for i in range(iterations):
        result = number_of_boxes(g, distances, num_nodes, diameter)
        results[i, :] = result[:]

    if debug:
        datetime = time.strftime("%d-%m-%Y_%H%M%S")
        filename = g.getName() + "_covering_" + datetime + ".csv"
        np.savetxt(filename, results, fmt='%i')

    boxes_length = np.arange(1, diameter+2)
    mean_nodes_per_box = results.mean(axis=0)

    # Fit a line and calculate the slope
    log_box_length = np.log(boxes_length)
    log_mean_number_of_nodes = np.log(mean_nodes_per_box)

    slope, intercept = np.polyfit(log_box_length, log_mean_number_of_nodes, 1)

    return math.fabs(slope)


def main(argv):
    infile = argv[0]
    graph = nk.readGraph(infile, nk.Format.GML)
    graph.setName(os.path.basename(infile))

    if graph.isDirected():
        graph = graph.toUndirected()

    print(fractal_dimension(graph, 1, True))


if __name__ == "__main__":
    main(sys.argv[1:])
