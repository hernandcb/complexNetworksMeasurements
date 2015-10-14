#!/usr/bin/python
# Author: Hernán David Carvajal <carvajal.hernandavid at gmail.com>
# Tested in python-3.4.3


import operator
import random as rnd
import networkit as nk
import networkx as nx
import pylab
import numpy as np
from pprint import pprint

centrality = {
    "degree": nk.centrality.DegreeCentrality,
    "closeness": nk.centrality.Closeness,
    "betweenness": nk.centrality.Betweenness,
    "eigenvector": nk.centrality.EigenvectorCentrality,
    "random": None
}


def largest_component_size(g):
    return len(sorted(nx.connected_components(g), key=len, reverse=True)[0])


def robustness(g, strategy="degree", sequential=True):
    """
    This method calculates the robustness index of the network by removing the
    nodes from the network and comparing the size of the largest component in
    the network to the number of nodes removed.

    Params
    ---------
    g:          networkx graph
    sequential: when false the ranking is updated each time a node is removed.
    strategy:   The strategy used to remove the nodes

    Return
    ----------
    vertices_removed: A list with the fraction of vertices removed
    component_size:   A list with the component size given a fraction of the
                      network removed
    robustness_index: The robustness index value
    """
    vertices_removed = []
    component_size = []
    n = len(g.nodes())
    r = 0.0
    rank = ranking(g, strategy)
    vertices_removed.append(0)
    component_size.append(largest_component_size(g)/n)

    for i in range(1, n):
        g.remove_node(rank.pop(0))
        print(largest_component_size(g) / n)
        r += largest_component_size(g) / n

        # print("vr: {}, cs: {}".format(i/n, largest_component_size(g)/n))
        vertices_removed.append(i / n)
        component_size.append(largest_component_size(g) / n)

        if not sequential:
            rank = ranking(g, strategy)

    print("R: ", r)
    return vertices_removed, component_size, (0.5 -(r / n))


def ranking(gx, measure="degree", reverse=False):
    """
    This method ranks the nodes of the graph from largest to smallest according
    to a given centrality measure

    Parameters
    -----------
    gx: A networkx graph
    measure: the centrality measure used to rank the nodes, the possible values
        are those present in the 'centrality' dictionary. Degree is the default
    reverse: if is set to true, the rank is ordered from smallest to largest.
             The default value is False

    Returns
    -----------
    A list of nodes ranked according to the centrality measure
    """
    # The networkx graph is converted to a networkit graph because that library
    # is more efficient calculating the centrality measures
    g = nk.nx2nk(gx)

    if measure is "random":
        nodes = g.nodes()
        rnd.shuffle(nodes)
        return nodes

    centrality_measure = centrality[measure](g).run()
    results = centrality_measure.ranking()
    results.sort(key=operator.itemgetter(1), reverse=not reverse)

    return [x[0] for x in results]


def main(g):
    pylab.figure(1, dpi=500)
    pylab.xlabel(r"Fraction of vertices removed ($\rho$)")
    pylab.ylabel(r"Fractional size of largest component ($\sigma$)")

    # Color generator
    color = iter(pylab.cm.rainbow(np.linspace(0, 1, len(centrality.keys()))))

    for strategy in centrality.keys():
        print(strategy)
        a, b, c = robustness(g.copy(), strategy)
        label = "%s ($R = %4.3f$)" % (strategy, c)
        pylab.plot(a, b, label=label, c=next(color), alpha=0.6, linewidth=2.0)

    pylab.legend(loc="upper right", shadow=False)
    pylab.savefig("test.pdf", format="pdf")
    pylab.close(1)


if __name__ == "__main__":
    # graph = nx.read_graph6("football.graph6")
    graph = nx.erdos_renyi_graph(100, 1)
    print(nx.number_of_nodes(graph))
    main(graph)
