#!/usr/bin/python
# Author: Hernán David Carvajal <carvajal.hernandavid at gmail.com>
# Tested in python-3.4.3
from _testbuffer import ndarray

import networkit as nk
import numpy as np

cimport cython
cimport numpy as np
from libc.stdlib cimport malloc, free, rand

DTYPE = np.int
ctypedef np.int_t DTYPE_t

cdef choose_color(set not_valid_colors, set valid_colors):
    """
    This method returns a value selected randomly from the values present in the
    set valid_colors which are not present in the list not_valid_coclealors.

    If there is no valid colors from the list, then it is returned the maximum
    value of both lists + 1


    Parameters
    -----------
    not_valid_colors: A list of not selectable numbers
    valid_colors: A list of selectable numbers
    """

    cdef list possible_values = list(valid_colors - not_valid_colors)
    cdef int i

    if possible_values:
        i = rand()%len(possible_values)-1
        if i == 0:
            i = 1

        return possible_values[i]
    else:
        return max(valid_colors.union(not_valid_colors)) + 1


@cython.boundscheck(False)
cdef np.ndarray[DTYPE_t, ndim=2] greedy_coloring(np.ndarray[DTYPE_t, ndim=2] distances, int num_nodes, int diameter):
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
    cdef int  i, lb, j, index, index2
    cdef np.ndarray[DTYPE_t, ndim=2] c = np.empty((num_nodes+1, diameter+2), dtype=DTYPE)

    cdef int *nodes
    nodes = <int *>malloc(num_nodes * cython.sizeof(int))

    cdef set valid_colors, not_valid_colors

    if nodes is NULL:
        raise MemoryError()

    c.fill(-1)
    # Matrix C will not use the 0 column and 0 row to
    # let the algorithm look very similar to the paper
    # pseudo-code

    for i from 0 <= i < num_nodes:
        nodes[i] = i+1

    # nodes = list(range(1, num_nodes+1))
    shuffle(nodes, num_nodes)

    c[nodes[0], :] = 0

    # Algorithm
    for index from 1 <= index < num_nodes:
        i = nodes[index]
        for lb from 2 <= lb < diameter:
            not_valid_colors = set()
            valid_colors = set()

            for index2 from 0 <= index2 < index:
                j = nodes[index2]

                if distances[i-1, j-1] >= lb:
                    not_valid_colors.add(c[j, lb])
                else:
                    valid_colors.add(c[j, lb])

            c[i, lb] = choose_color(not_valid_colors, valid_colors)

    with nogil:
        free(nodes)
    return c


cdef int * shuffle(int *lst, int size):
  '''A modern Fisher-Yates shuffle popularized by Knuth.
  '''
  cdef int i, j

  for i in range(size-1, -1, -1):
    if i == 0:
        j =0
    else:
        j = rand() % i
    lst[j], lst[i] = lst[i], lst[j]
  return lst


cpdef np.ndarray[DTYPE_t, ndim=2] all_pairs_shortest_path_length(g):
    """
    This method creates a matrix containing all the shortest paths distances
    between each pair of nodes in the network. If not exists a path between two
    nodes then their distance is -1.

    Parameters
    ------------
    A networkit graph

    Returns
    ------------
    a matrix containing all the shortest paths distances.
    """
    import sys

    cdef int i, j
    cdef int n = g.numberOfNodes()
    cdef list row_distances
    cdef np.ndarray[DTYPE_t, ndim=2] distances = np.zeros((n, n), dtype=DTYPE)

    for i in range(n):
        bfs = nk.graph.BFS(g, i).run()
        row_distances = bfs.getDistances()

        for j from 0 <= j < len(distances):
            if row_distances[j] != sys.float_info.max:
                distances[i, j] = row_distances[j]
            else:
                distances[i, j] = -1

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

    cdef np.ndarray[DTYPE_t, ndim=2] c = greedy_coloring(distances, num_nodes, diameter)
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


cpdef list number_of_boxes(g, np.ndarray[DTYPE_t, ndim=2] distances, int num_nodes, int diameter):
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
    cdef np.ndarray[DTYPE_t, ndim=2] c = greedy_coloring(distances, num_nodes, diameter)
    cdef int lb

    cdef list boxes = []
    # When the box size is one, the number of boxes is equal to the number of nodes
    boxes.append(num_nodes)

    for lb from 2 <= lb <= diameter:
        boxes.append(np.unique(c[:, lb]).size - 1)

    # When the box size is bigger than the diameter all the nodes are placed in the same box
    boxes.append(1)

    return boxes


@cython.boundscheck(False)
def test(G):
    """
    _boxes = box_covering(G)
    for _box in _boxes:
        print(_box)
    """

    if G.isDirected():
        G = G.toUndirected()

    cdef int num_nodes = G.numberOfNodes()
    cdef np.ndarray[DTYPE_t, ndim=2] distances = all_pairs_shortest_path_length(G)
    cdef int diameter = np.amax(distances)

    # print(number_of_boxes(G, distances, num_nodes, diameter))


if __name__ == '__main__':
    G = nk.Graph()
    for i in range(6):
        G.addNode()

    G.addEdge(0, 4)
    G.addEdge(0, 5)
    G.addEdge(1, 2)
    G.addEdge(1, 3)
    G.addEdge(2, 5)
    G.addEdge(4, 5)

    _boxes = box_covering(G)
    for _box in _boxes:
        print(_box)

    # print(number_of_boxes(G))
