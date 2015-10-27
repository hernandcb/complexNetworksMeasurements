#!/usr/bin/python
# Author: Hernán David Carvajal <carvajal.hernandavid at gmail.com>
# Tested in python-3.4.3


import operator
import random as rnd
import networkit as nk
import pylab
import numpy as np
import time

centrality = {
    "degree": nk.centrality.DegreeCentrality,
    "closeness": nk.centrality.Closeness,
    "betweenness": nk.centrality.Betweenness,
    "eigenvector": nk.centrality.EigenvectorCentrality,
    "random": None
}


def average_shortest_path_length(g):
    """
    TODO - Specify that this method also works with disconnected networks but
    i'm not sure if it does in the proper way

    """
    import sys
    n = g.numberOfNodes()
    avg = 0.0

    if n == 0:
        return 0.0

    for node in g.nodes():
        dijkstra = nk.graph.Dijkstra(g, node).run()
        avg += sum(filter(lambda a: a != sys.float_info.max, dijkstra.getDistances()))

    return avg / (n*(n-1))


def largest_component_size(g):
    components_size = nk.properties.components(g)[1]
    return sorted(components_size.items(), key=operator.itemgetter(1), reverse=True)[0][1]


comparative_measures = {
    "component_size": largest_component_size,
    "path_length": average_shortest_path_length
}


base_values = {
    "component_size": nk.Graph.numberOfNodes,
    # The path length is not compared against anything
    "path_length": lambda x: 1
}


def remove_node(network, node):
    """
    This method removes a node from the network. To do so, it first removes all
    the edges adjacent to the node to be removed.

    Params
    --------
    network: networkit graph
    node:    node identifier
    """
    for neighbor in network.neighbors(node):
        network.removeEdge(node, neighbor)
    network.removeNode(node)


def calculate(g, strategy="degree", measure="component_size", sequential=True):
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
    comparative_measure_values:   A list with the comparative measure values
                          (i.e. component size or avg path length) given a
                          fraction of the network removed
    robustness_index: The robustness index value
    """
    vertices_removed = []
    comparative_measure_values = []

    base_value = base_values[measure](g)
    n = len(g.nodes())
    r = 0.0

    rank = ranking(g, strategy)
    vertices_removed.append(0)
    comparative_measure_values.append(comparative_measures[measure](g)/base_value)

    for i in range(1, n-1):
        remove_node(g, rank.pop(0))
        comparative_value = comparative_measures[measure](g)
        r += comparative_value / n

        # print("vr: {}, cs: {}".format(i/n, largest_component_size(g)/n))
        vertices_removed.append(i / n)
        comparative_measure_values.append(comparative_value / base_value)

        if not sequential:
            rank = ranking(g, strategy)

    return vertices_removed, comparative_measure_values, (r / n)


def ranking(g, measure="degree", reverse=False):
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
    if measure is "random":
        nodes = g.nodes()
        rnd.shuffle(nodes)
        return nodes

    centrality_measure = centrality[measure](g).run()
    results = centrality_measure.ranking()
    results.sort(key=operator.itemgetter(1), reverse=not reverse)

    return [x[0] for x in results]


def plot_robustness_analysis(g, debug=True):
    """
    Compute the robustness analysis on a network and plot the results

    Params
    ---------
    g: Networkit graph
    """

    fig = pylab.figure(1, dpi=500)

    current_time = time.strftime("%d-%m-%Y_%H%M%S")
    file_name = g.getName() + "_robustness_analysis_" + "_" + current_time

    index = 1
    for name, comparative_measure in comparative_measures.items():
        for sequential_analysis in [True, False]:
            method_name = "robustness_" + name + "_"
            method_name += "sequential" if sequential_analysis else "simultaneous"

            if debug:
                file_results = open(file_name + ".results", 'a')

            analysis_plot = fig.add_subplot(2,2, index)
            analysis_plot.set_xlabel(r"Fraction of vertices removed ($\rho$)")
            analysis_plot.set_ylabel(r"Fractional size of " + name + " ($\sigma$)")
            analysis_plot.legend(loc="upper right", shadow=False)

            # Color generator
            color = iter(pylab.cm.rainbow(np.linspace(0, 1, len(centrality.keys()))))

            print("----------------------------------------", file=file_results)
            print(method_name, file=file_results)
            for strategy in centrality.keys():
                vertices_removed, component_size, r_index = calculate(nk.Graph(g), strategy, name, sequential_analysis)
                label = "%s ($R = %4.3f$)" % (strategy, r_index)
                analysis_plot.plot(vertices_removed, component_size, label=label, c=next(color), alpha=0.6, linewidth=2.0)

                if debug:
                    print("{} {}".format(strategy, r_index), file=file_results)

            index += 1

    pylab.tight_layout()
    pylab.savefig(file_name + ".png", format="png")
    pylab.close(1)

    if debug:
        file_results.close()


if __name__ == "__main__":
    graph = nk.readGraph("football.gml", nk.Format.GML)

    #erg = nk.generators.ErdosRenyiGenerator(10, 0.3, False)
    #graph = erg.generate()

    plot_robustness_analysis(graph)
