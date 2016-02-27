#!/usr/bin/python
# Author: Hernán David Carvajal <carvajal.hernandavid at gmail.com>
# Tested in python-3.4.3

import sys
import os
import time
import math

import pyximport
pyximport.install()

from .boxCovering.cythonGreedyColoring import *


def fractal_dimension(g, iterations=1000, debug=True):
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
    diameter = int(nk.distance.Diameter.exactDiameter(g))
    num_nodes = g.numberOfNodes()
    results = np.empty((iterations, diameter+1), dtype=int)

    # print("Results: \n", len(results))

    for i in range(iterations):
        if diameter > 0:
            result = number_of_boxes(g)
        else:
            result = [num_nodes]
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


def main(n=100, iterations=100):

    import networkx as nx
    g = nk.nxadapter.nx2nk(nx.erdos_renyi_graph(n, 0.6))

    print(fractal_dimension(g, iterations, False))


if __name__ == "__main__":
    main()
