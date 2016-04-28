#!/usr/bin/python
# Author: Hernán David Carvajal <carvajal.hernandavid at gmail.com>
# Tested in python-3.4.3

import sys
import os
import time
import math
import networkit as nk
import numpy as np
from scipy import stats

"""
import pyximport
pyximport.install()

from .boxCovering.cythonGreedyColoring import *
#from .boxCovering.greedyColoring import *
"""

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

        if len(results[i, :]) == len(result[:]):
            results[i, :] = result[:]
        else:
            difference = len(results[i, :]) - len(result[:])
            otra = [1 for i in range(difference)]
            result[:].extend(otra)
            results[i, :] = otra

    if debug:
        datetime = time.strftime("%d-%m-%Y_%H%M%S")
        filename = g.getName() + "_covering_" + datetime + ".csv"
        np.savetxt(filename, results, fmt='%i')

    boxes_length = np.arange(1, diameter+2)
    mean_nodes_per_box = results.mean(axis=0)

    # If there is only on point in the data, it has not slope
    if len(boxes_length) is 1:
        return np.NaN;

    # Fit a line and calculate the slope
    log_box_length = np.log(boxes_length)
    log_mean_number_of_nodes = np.log(mean_nodes_per_box)

    #slope, intercept = np.polyfit(log_box_length, log_mean_number_of_nodes, 1)

    # """
    # Use this to calculate the fit error

    sslope, sintercept, sr_value, sp_value, sstd_err = stats.linregress(log_box_length,log_mean_number_of_nodes)
    print("scipy dimension: {}, error: {}".format( math.fabs(sslope), 1 - sr_value**2 ))

    if len(boxes_length) is 2:
        # There is no error fitting a line to connect two points
        slope, intercept = np.polyfit(log_box_length, log_mean_number_of_nodes, 1)
    else:
        p, cov = np.polyfit(log_box_length, log_mean_number_of_nodes, 1, cov=True)
        slope = p[0]
        print("numpy dimension: {}, error: {}".format( math.fabs(slope), np.sqrt(np.diag(cov))**2 ))
    # """

    return math.fabs(slope)

def number_of_boxes(g):
    """
    This method computes the boxes required to cover a graph with all the
    possible box sizes.
    If the optional parameters are not passed they are calculated.

    Parameters
    -------------------
    G:          Networkit graph

    Returns
    ------------------
    This method returns a dictionary specifying the number of boxes found for
    every box length:   { box_length: number_of_boxes}

    """

    diameter = int(nk.distance.Diameter.exactDiameter(g))
    num_nodes = g.numberOfNodes()
    #print("--------------------------")
    c = np.array(g.greedyColoring())
    #print("++++++++++++++++++++++++++")

    boxes = []
    for lb in range(1, diameter+2):
        if lb is 1:
            # Each node is in a different box
            boxes.append(num_nodes)
        elif lb == diameter + 1:
            # Every node is in the same box
            boxes.append(1)
        else:
            boxes.append(len(np.unique(c[:, lb-1])) - 1)

    return boxes


def main(n=10, iterations=1):

    import networkx as nx
    g = nk.nxadapter.nx2nk(nx.erdos_renyi_graph(n, 0.6))

    print(fractal_dimension(g, iterations, False))


if __name__ == "__main__":
    main()
