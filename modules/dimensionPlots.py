"""
NAME
      DimensionPlots

DESCRIPTION
      This script plots the variation of the fractal dimension on a network
      when the nodes are removed. The node to be removed is chosen according to
      its centrality measure (degree, betweennes, closeness) or randomly.

      This script generates two files:
      - A csv file containing the data
      - A png file where the data is plotted

      Code tested on Python 3.4

PARAMETERS
       This script should be called as:

       > dimensionPlots.py infile outfile.png recalculate

       infile:      The gml file where the network is stored
       outfile:     The name of the file where the data will be saved. The
                    png file produced will have the same name
       recalculate: [True ¡ False ] Indicates if the centrality measures
                    should be updated each time a node is removed.

       example:
            > python dimensionPlots.py karate.gml karate.png False

AUTHOR
      Hernán D. Carvajal
"""

import sys
import random
import operator
import networkx as nx
import pylab
import dimension.fractalDimension as fd


def remove_nodes(g, selection_method, recalculate=False):
    """
    This method removes nodes of a network according to the ranking generated
    by selection_method. When the parameter recalculate is True the ranking
    is updated each time a node is removed.

     Parameters
    -------------------
    G:          Networkx graph
    selection_method:  Method that ranks the nodes in G according to some
                criterium and returns a dictionary with the format:
                { nodeID: classificationValue }
    recalculate:   This indicates if the ranking should be updated each time
                    a node is removed.

    Returns
    ------------------
    x:    A list indicating the fraction of nodes removed
    y:    y[i] contains the fractal dimension of the network when a fraction
          x[i] of the network has been removed.
    """

    m = selection_method(g)
    l = sorted(m.items(), key=operator.itemgetter(1), reverse=True)
    x = []
    y = []

    dimension = fd.fractal_dimension(g, iterations=100, debug=False)

    n = len(g.nodes())
    x.append(0)
    y.append(dimension)

    for i in range(1, n-1):
        g.remove_node(l.pop(0)[0])
        if recalculate:
            m = selection_method(g)
            l = sorted(m.items(), key=operator.itemgetter(1),
                       reverse=True)

        dimension = fd.fractal_dimension(g, iterations=100, debug=False)
        x.append(i * 1. / n)
        y.append(dimension)

    return x, y


def random_ranking(g):
    nodes = g.nodes()
    values = g.nodes()
    random.shuffle(values)

    return dict(zip(nodes, values))


def plot_functions(g, outfile, recalculate=False):
    x1, y1 = remove_nodes(g.copy(), nx.degree_centrality, recalculate)
    x2, y2 = remove_nodes(g.copy(), nx.betweenness_centrality, recalculate)
    x3, y3 = remove_nodes(g.copy(), nx.closeness_centrality, recalculate)
    x5, y5 = remove_nodes(g.copy(), random_ranking, recalculate)

    pylab.figure(1, dpi=500)
    pylab.xlabel(r"Fraction of vertices removed ($\rho$)")
    pylab.ylabel(r"Fractal dimension ($\sigma$)")

    pylab.plot(x1, y1, "b-", alpha=0.6, linewidth=2.0)
    pylab.plot(x2, y2, "g-", alpha=0.6, linewidth=2.0)
    pylab.plot(x3, y3, "r-", alpha=0.6, linewidth=2.0)
    pylab.plot(x5, y5, "k-", alpha=0.6, linewidth=2.0)

    pylab.legend((r"Degree",
                  "Betweenness",
                  "Closeness",
                  "Random"),
                  loc="upper right", shadow=False)

    pylab.savefig(outfile, format="png")
    pylab.close(1)

    # Generate csv file
    import numpy as np
    matrix = np.matrix([x1, y1, y2, y3, y5])

    filename = outfile.rsplit(".", 1)[0] + ".csv"
    header = ", degree, betweeness, closeness, random"
    separator = ", "

    np.savetxt(filename, matrix.transpose(), fmt="%s", delimiter=separator,
               header=header, comments="")


if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]

    if sys.argv[3] == "True":
        recalculate = True
    else:
        recalculate = False

    # The file is readed using networkit because there are memory issues with
    # the networkx gml reader.
    import networkit as nk
    gk = nk.readGraph(infile, nk.Format.GML)
    g = nk.nk2nx(gk)

    plot_functions(g, outfile, recalculate)
