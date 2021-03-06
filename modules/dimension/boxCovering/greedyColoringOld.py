#!/usr/bin/python
# Author: Hernán David Carvajal <carvajal.hernandavid at gmail.com>
# Tested in python-3.4.3

import networkit as nk
import numpy as np
import random as rnd


def choose_color(not_valid_colors, valid_colors):
    """
    This method returns a value selected randomly from the values present in the
    set valid_colors which are not present in the list not_valid_colors.

    If there is no valid colors from the list, then it is returned the maximum
    value of both lists + 1


    Parameters
    -----------
    not_valid_colors: A list of not selectable numbers
    valid_colors: A list of selectable numbers
    """

    possible_values = list(valid_colors - not_valid_colors)

    if possible_values:
        return rnd.choice(possible_values)
    else:
        return max(valid_colors.union(not_valid_colors)) + 1


def greedy_coloring(distances, num_nodes, diameter):
    """
    Compute the minimal set of boxes to cover a graph given a box length.
    This method uses the box values between [2, network_diameter]

    Parameters
    -------------------
    distances:  Matrix containing all the shortest path lengths between all
                nodes in a graph.
    num_nodes:  Number of nodes in the graph
    diameter:   Diameter of the graph

    References:
    Chaoming Song, Lazaros K Gallos, Shlomo Havlin, and Hernán A Makse.
    How to calculate the fractal dimension of a complex network: the box cov-
    ering algorithm. Journal of Statistical Mechanics: Theory and Experiment,
    2007(03):P03006, 2007.
    http://iopscience.iop.org/1742-5468/2007/03/P03006/
    """

    c = np.empty((num_nodes+1, diameter+2), dtype=int)
    c.fill(-1)
    # Matrix C will not use the 0 column and 0 row to
    # let the algorithm look very similar to the paper
    # pseudo-code

    nodes = list(range(1, num_nodes+1))
    rnd.shuffle(nodes)

    c[nodes[0], :] = 0

    # Algorithm
    for i in nodes[1:]:
        for lb in range(2, diameter+1):
            not_valid_colors = set()
            valid_colors = set()

            for j in nodes[:i]:

                if distances[i-1, j-1] >= lb:
                    not_valid_colors.add(c[j, lb])
                else:
                    valid_colors.add(c[j, lb])

                c[i, lb] = choose_color(not_valid_colors, valid_colors)

    return c


def all_pairs_shortest_path_length(g):
    """
    This method creates a matrix containing all the shortest paths distances
    between each pair of nodes in the network.

    Parameters
    ------------
    A networkit graph

    Returns
    ------------
    a matrix containing all the shortest paths distances.
    """
    n = g.numberOfNodes()

    if n >= 65535:
        distances = np.zeros((n, n), dtype=np.uint32)
    else:
        distances = np.zeros((n, n), dtype=np.uint16)

    for i in range(n):
        bfs = nk.graph.BFS(g, i).run()
        distances[i, :] = np.array(bfs.getDistances())

    return distances


def box_covering(g, distances=None, num_nodes=None, diameter=None):
    """
    This method computes the boxes required to cover a graph with all the
    possible box sizes.
    If the optional parameters are not passed they are calculated.

    This method returns a list of dictionaries with
    { box_id: subgraph generated by the nodes in this box}


    Parameters
    -------------------
    G:          Networkit graph
    distances:  Matrix containing all the shortest path lengths between all
                nodes in ``G``
    num_nodes:  Number of nodes in the graph
    diameter:   Diameter of the graph

    """

    if num_nodes is None:
        num_nodes = g.numberOfNodes()

    if distances is None:
        distances = all_pairs_shortest_path_length(g)

    if diameter is None:
        diameter = np.amax(distances)

    c = greedy_coloring(distances, num_nodes, diameter)

    # Creation of boxes by color
    boxes = []
    for LB in range(1, diameter+2):
        box = {}  # each box is a dictionary (color: [nodes])
        for j in range(1, num_nodes+1):
            if LB is 1:
                # Each node is in a different box
                box[j] = box.get(j, [])
                box[j].append(j)
            elif LB == diameter + 1:
                # Every node is in the same box
                box[1] = box.get(1, [])
                box[1].append(j)
            else:
                color = c[j, LB]
                box[color] = box.get(color, [])
                box[color].append(j)

        boxes.append(box)

    return boxes


def number_of_boxes(g, distances=None, num_nodes=None, diameter=None):
    """
    This method computes the boxes required to cover a graph with all the
    possible box sizes.
    If the optional parameters are not passed they are calculated.

    Parameters
    -------------------
    G:          Networkit graph
    distances:  Matrix containing all the shortest path lengths between all
                nodes in ``G``
    num_nodes:  Number of nodes in the graph
    diameter:   Diameter of the graph

    Returns
    ------------------
    This method returns a dictionary specifying the number of boxes found for
    every box length:   { box_length: number_of_boxes}

    """

    if num_nodes is None:
        num_nodes = g.numberOfNodes()

    if distances is None:
        distances = all_pairs_shortest_path_length(g)

    print(np.amax(distances))
    if diameter is None:
        diameter = np.amax(distances)

    c = greedy_coloring(distances, num_nodes, diameter)

    boxes = []
    for lb in range(1, diameter+2):
        if lb is 1:
            # Each node is in a different box
            boxes.append(num_nodes)
        elif lb == diameter + 1:
            # Every node is in the same box
            boxes.append(1)
        else:
            boxes.append(len(np.unique(c[:, lb])) - 1)

    return boxes


def test(G):
    """
    _boxes = box_covering(G)
    for _box in _boxes:
        print(_box)
    """

    if G.isDirected():
        G = G.toUndirected()

    number_of_boxes(G)
    # print(number_of_boxes(G))
