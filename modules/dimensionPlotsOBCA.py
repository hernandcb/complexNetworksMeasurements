import sys
import random
import operator
import networkx as nx
import pylab
import dimension.fractalDimension as fd


def betweenness_removal(g, recalculate=False):
    """
    Performs robustness analysis based on betweenness centrality,
    on the network specified by infile using sequential (recalculate = True)
    or simultaneous (recalculate = False) approach. Returns a list
    with fraction of nodes removed, a list with the corresponding sizes of
    the largest component of the network, and the overall vulnerability
    of the network.
    """

    m = nx.betweenness_centrality(g)
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
            m = nx.betweenness_centrality(g)
            l = sorted(m.items(), key=operator.itemgetter(1),
                       reverse=True)

        dimension = fd.fractal_dimension(g, iterations=100, debug=False)
        x.append(i * 1. / n)
        y.append(dimension)

    return x, y


def closeness_removal(g, recalculate=False):
    """
    Performs robustness analysis based on closeness centrality,
    on the network specified by infile using sequential (recalculate = True)
    or simultaneous (recalculate = False) approach. Returns a list
    with fraction of nodes removed, a list with the corresponding sizes of
    the largest component of the network, and the overall vulnerability
    of the network.
    """

    m = nx.closeness_centrality(g)
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
            m = nx.closeness_centrality(g)
            l = sorted(m.items(), key=operator.itemgetter(1),
                       reverse=True)
        dimension = fd.fractal_dimension(g, iterations=100, debug=False)
        x.append(i * 1. / n)
        y.append(dimension)

    return x, y


def degree_removal(g, recalculate=False):
    """
    Performs robustness analysis based on degree centrality,
    on the network specified by infile using sequential (recalculate = True)
    or simultaneous (recalculate = False) approach. Returns a list
    with fraction of nodes removed, a list with the corresponding sizes of
    the largest component of the network, and the overall vulnerability
    of the network.
    """

    m = nx.degree_centrality(g)
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
            m = nx.degree_centrality(g)
            l = sorted(m.items(), key=operator.itemgetter(1),
                       reverse=True)
        dimension = fd.fractal_dimension(g, iterations=100, debug=False)
        x.append(i * 1. / n)
        y.append(dimension)

    return x, y


def random_removal(g):

    nodes = g.nodes()
    random.shuffle(nodes)
    x = []
    y = []

    dimension = fd.fractal_dimension(g, iterations=100, debug=False)
    n = len(nodes)

    x.append(0)
    y.append(dimension)
    r = 0.0

    for i in range(1, n):
        g.remove_node(nodes.pop(0))
        dimension = fd.fractal_dimension(g, iterations=100, debug=False)

        x.append(i * 1. / n)
        y.append(dimension)

    return x, y


def plot_functions(g, outfile, recalculate=False):
    x1, y1 = degree_removal(g.copy(), recalculate)
    x2, y2 = betweenness_removal(g.copy(), recalculate)
    x3, y3 = closeness_removal(g.copy(), recalculate)
    # x4, y4, VE = eigenvector(g.copy(), recalculate)
    x5, y5 = random_removal(g.copy())

    pylab.figure(1, dpi=500)
    pylab.xlabel(r"Fraction of vertices removed ($\rho$)")
    pylab.ylabel(r"Fractal dimension ($\sigma$)")

    pylab.plot(x1, y1, "b-", alpha=0.6, linewidth=2.0)
    pylab.plot(x2, y2, "g-", alpha=0.6, linewidth=2.0)
    pylab.plot(x3, y3, "r-", alpha=0.6, linewidth=2.0)
    # pylab.plot(x4, y4, "c-", alpha=0.6, linewidth=2.0)
    pylab.plot(x5, y5, "k-", alpha=0.6, linewidth=2.0)

    pylab.legend((r"Degree",
                  "Betweenness",
                  "Closeness",
                  # "Eigenvector ($R = %4.3f$)" % VE,
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

    import networkit as nk

    gk = nk.readGraph(infile, nk.Format.GML)
    g = nk.nk2nx(gk)
    # g = nx.read_gml(infile)

    plot_functions(g, outfile, recalculate)
