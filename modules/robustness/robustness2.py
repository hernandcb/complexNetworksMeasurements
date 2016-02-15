#!/usr/bin/python
"""
NAME
      Robustness

DESCRIPTION
      This script compute the robustness of a network by removing all the
      nodes (the selection criteria used are the centrality measures) and
      measuring the giant component size or the average path length as it is
      presented in:

      http://www.ncbi.nlm.nih.gov/pubmed/23565156

      This script generates two files:
      - A csv file containing the data
      - A png file where the data is plotted

      Code tested on Python 3.4

PARAMETERS
       This script should be called as:

       > robustness.py infile outfile.png apl recalculate

       infile:       The gml file where the network is stored
       outfile:      The name of the file where the data will be saved. The png
                     file produced will have the same name
       apl:          [apl ¡ component] Indicates if the base measure is the
                     average path length. Otherwise the size of the giant
                     component is used.
       recalculate:  Indicate if the centrality measures should be updated
                     each time a node is removed.

       example:
            > python robustness2.py karate.gml karate.png apl False

AUTHOR
      Hernán D. Carvajal
"""

import networkx as nx
import operator
import pylab
import random
import sys


def robustness_analysis(g, node_classifier, recalculate=False):
    m = node_classifier(g)
    l = sorted(m.items(), key=operator.itemgetter(1), reverse=True)
    x = []
    y = []

    largest_component = max(nx.connected_components(g), key=len)

    n = len(g.nodes())
    x.append(0)
    y.append(len(largest_component) * 1. / n)
    r = 0.0
    for i in range(1, n-1):
        g.remove_node(l.pop(0)[0])
        if recalculate:
            m = node_classifier(g)
            l = sorted(m.items(), key=operator.itemgetter(1),
                       reverse=True)
        largest_component = max(nx.connected_components(g), key=len)
        x.append(i * 1. / n)
        r += len(largest_component) * 1. / n
        y.append(len(largest_component) * 1. / n)
    return x, y, r / n


def robustness_analysis_apl(g, node_classifier, recalculate=False):
    m = node_classifier(g)
    l = sorted(m.items(), key=operator.itemgetter(1), reverse=True)
    x = []
    y = []

    average_path_length = 0.0
    number_of_components = 0
    n = len(g.nodes())

    for sg in nx.connected_component_subgraphs(g):
        average_path_length += nx.average_shortest_path_length(sg)
        number_of_components += 1

    average_path_length = average_path_length / number_of_components
    initial_apl = average_path_length

    x.append(0)
    y.append(average_path_length * 1. / initial_apl)
    r = 0.0
    for i in range(1, n-1):
        g.remove_node(l.pop(0)[0])
        if recalculate:
            m = node_classifier(g)
            l = sorted(m.items(), key=operator.itemgetter(1),
                       reverse=True)

        average_path_length = 0.0
        number_of_components = 0

        for sg in nx.connected_component_subgraphs(g):
            if len(sg.nodes()) > 1:
                average_path_length += nx.average_shortest_path_length(sg)
            number_of_components += 1

        average_path_length = average_path_length / number_of_components

        x.append(i * 1. / n)
        r += average_path_length * 1. / initial_apl
        y.append(average_path_length * 1. / initial_apl)
    return x, y, r / n


def random_ranking(g):
    nodes = g.nodes()
    values = g.nodes()
    random.shuffle(values)

    return dict(zip(nodes, values))


def main(argv):
    """
    Entry point.
    """

    if len(argv) != 4:
        print("python robustness.py <infile> <outfile> <measure>[component ¡ apl] <recalculate>")
        sys.exit(0)

    infile = argv[0]
    outfile = argv[1]

    if argv[2] == "apl":
        apl = True
        analysis_method = robustness_analysis_apl
    else:
        apl = False
        analysis_method = robustness_analysis

    if argv[3] == "True":
        recalculate = True
    else:
        recalculate = False

    g = nx.read_gml(infile).to_undirected()
    x1, y1, vd = analysis_method(g.copy(), nx.degree_centrality, recalculate)
    x2, y2, vb = analysis_method(g.copy(), nx.betweenness_centrality, recalculate)
    x3, y3, vc = analysis_method(g.copy(), nx.closeness_centrality, recalculate)
    x5, y5, vr = analysis_method(g.copy(), random_ranking)

    if not apl:
        pylab.figure(1, dpi=500)
        pylab.xlabel(r"Fraction of vertices removed ($\rho$)")
        pylab.ylabel(r"Fractional size of largest component ($\sigma$)")
    else:
        pylab.figure(1, dpi=500)
        pylab.xlabel(r"Fraction of vertices removed ($\rho$)")
        pylab.ylabel(r"Average path length ($\sigma$)")

    pylab.plot(x1, y1, "b-", alpha=0.6, linewidth=2.0)
    pylab.plot(x2, y2, "g-", alpha=0.6, linewidth=2.0)
    pylab.plot(x3, y3, "r-", alpha=0.6, linewidth=2.0)
    pylab.plot(x5, y5, "k-", alpha=0.6, linewidth=2.0)

    # Generate csv file
    import numpy as np

    pylab.legend((r"Degree ($R = %4.3f$)" % vd,
                  "Betweenness ($R = %4.3f$)" % vb,
                  "Closeness ($R = %4.3f$)" % vc,
                  "Random ($R = %4.3f$)" % vr),
                  loc="upper right", shadow=False)

    pylab.savefig(outfile, format="png")
    pylab.close(1)

    matrix = np.matrix([x1, y1, y2, y3, y5])
    filename = outfile.rsplit(".", 1)[0] + ".csv"
    header = " , degree, betweeness, closeness, random"
    separator = ", "

    np.savetxt(filename, matrix.transpose(), fmt="%2.5f", delimiter=separator,
              header=header, comments="")


if __name__ == "__main__":
    main(sys.argv[1:])
