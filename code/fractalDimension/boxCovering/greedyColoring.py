#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Andrés Becerra sandoval <andres.becerra at gmail.com>
# Modified by:  Hernán David Carvajal <carvajal.hernandavid at gmail.com>
# Tested in python-3.4.2 

from __future__ import print_function
from random import shuffle
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def different(Colors):
    """ Returns a different color from all given in
        the input
        Key arguments: Colors, list of integers representing colors
    """
    j = 0
    while(True):
        if j not in Colors:
            return j
        j = j+1
        


def greedyColoring(G, randomized=False):
    """
    Compute the minimal set of boxes to cover a graph,
    from the paper:
    Chaoming Song, Lazaros K Gallos, Shlomo Havlin, and Hernán A Makse.
    How to calculate the fractal dimension of a complex network: the box cov-
    ering algorithm. Journal of Statistical Mechanics: Theory and Experiment,
    2007(03):P03006, 2007.
    http://iopscience.iop.org/1742-5468/2007/03/P03006/
    """
    num_nodes = nx.number_of_nodes(G)
    diameter = nx.diameter(G)
    distances = nx.all_pairs_shortest_path_length(G)
    
    C = np.empty( (num_nodes+1,diameter+2),dtype=int)
    C.fill(-1)

    # Matrix C will not use the 0 column and 0 row to
    # let the algorithm look very similar to the paper
    # pseudocode

    # Create a random list with the node indexes
    nodes = list(range(1,num_nodes+1))
    if randomized:
        shuffle(nodes)

    for j in range(diameter+2):
        C[nodes[0]][j] = 0
    
    # Algorithm
    for i in nodes[1:]: #2 .. num_nodes
        for LB in range(1,diameter+2): # 1..diameter+1
            colors = []

            for j in nodes:  # 1..i-1
                if j == i: break;
                if distances[i-1][j-1] >= LB:
                    colors.append( C[j][LB])
            
            newcolor = different(colors)
            C[i][LB] = newcolor


    for j in range(1,num_nodes+1):
        n = C.max(axis=0)

    # Creation of boxes by color
    boxes = []
    for LB in range(1,diameter+2):
        box = {} # each box is a dictionary (color, [nodes])
        for j in range(1,num_nodes+1):
            color = C[j][LB]
            box[color] = box.get(color,[])
            box[color].append(j)
        boxes.append(box)
    
    return boxes
        
if __name__ == '__main__':
    G = nx.Graph()
    G.add_nodes_from([0,1,2,3,4,5])
    G.add_edges_from([(0,4), (0,5), (1,2), (1,3), (2,5), (4,5)])
    boxes = greedyColoring(G, True)
    for box in boxes:
        print(box)
        
    print( len(boxes[0]) )
