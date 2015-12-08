#!/usr/bin/python

"""
This script performs robustness analysis on the given network, 
which involves removing nodes from the network at random, or in reverse 
order of centrality measures (degree, betweenness, closeness, and 
eigenvector), and comparing the size of the largest component in the 
network to the fraction of nodes removed.

Usage: python robustness.py <infile> <outfile> <recalculate>

where infile is the name of the network file in gml format, outfile is the 
name of the output (pdf) file in which the results of the analysis is 
saved, and recalculate (True of False) specifies if the targeted attack is 
simultaneous (False), or sequential (True).
"""

import networkx
import numpy
import operator
import pylab
import random
import sys


def betweenness(g, recalculate=False):
    """
    Performs robustness analysis based on betweenness centrality,  
    on the network specified by infile using sequential (recalculate = True) 
    or simultaneous (recalculate = False) approach. Returns a list 
    with fraction of nodes removed, a list with the corresponding sizes of 
    the largest component of the network, and the overall vulnerability 
    of the network.
    """

    m = networkx.betweenness_centrality(g)
    l = sorted(m.items(), key=operator.itemgetter(1), reverse=True)
    x = []
    y = []

    largest_component = max(networkx.connected_components(g), key=len)
    
    n = len(g.nodes())
    x.append(0)
    y.append(len(largest_component) * 1. / n)
    r = 0.0
    for i in range(1, n):
        g.remove_node(l.pop(0)[0])
        if recalculate:
            m = networkx.betweenness_centrality(g)
            l = sorted(m.items(), key=operator.itemgetter(1), 
                       reverse=True)
        largest_component = max(networkx.connected_components(g), key=len)
        x.append(i * 1. / n)
        r += len(largest_component) * 1. / n
        y.append(len(largest_component) * 1. / n)
    return x, y, r / n


def betweenness_apl(g, recalculate=False):
    """
    Performs robustness analysis based on betweenness centrality,
    on the network specified by infile using sequential (recalculate = True)
    or simultaneous (recalculate = False) approach. Returns a list
    with fraction of nodes removed, a list with the corresponding sizes of
    the largest component of the network, and the overall vulnerability
    of the network.
    """

    m = networkx.betweenness_centrality(g)
    l = sorted(m.items(), key=operator.itemgetter(1), reverse=True)
    x = []
    y = []

    average_path_length = 0.0
    number_of_components = 0
    n = len(g.nodes())

    for sg in networkx.connected_component_subgraphs(g):
        average_path_length += networkx.average_shortest_path_length(sg)
        number_of_components += 1

    average_path_length = average_path_length / number_of_components
    initial_apl = average_path_length

    x.append(0)
    y.append(average_path_length * 1. / initial_apl)
    r = 0.0
    for i in range(1, n):
        g.remove_node(l.pop(0)[0])
        if recalculate:
            m = networkx.betweenness_centrality(g)
            l = sorted(m.items(), key=operator.itemgetter(1),
                       reverse=True)

        average_path_length = 0.0
        number_of_components = 0

        for sg in networkx.connected_component_subgraphs(g):
            if len(sg.nodes()) > 1:
                average_path_length += networkx.average_shortest_path_length(sg)
            number_of_components += 1

        average_path_length = average_path_length / number_of_components

        x.append(i * 1. / initial_apl)
        r += average_path_length
        y.append(average_path_length)
    return x, y, r / initial_apl


def closeness(g, recalculate=False):
    """
    Performs robustness analysis based on closeness centrality,  
    on the network specified by infile using sequential (recalculate = True) 
    or simultaneous (recalculate = False) approach. Returns a list 
    with fraction of nodes removed, a list with the corresponding sizes of 
    the largest component of the network, and the overall vulnerability 
    of the network.
    """

    m = networkx.closeness_centrality(g)
    l = sorted(m.items(), key=operator.itemgetter(1), reverse=True)
    x = []
    y = []
    largest_component = max(networkx.connected_components(g), key=len)
    n = len(g.nodes())
    x.append(0)
    y.append(len(largest_component) * 1. / n)
    r = 0.0
    for i in range(1, n):
        g.remove_node(l.pop(0)[0])
        if recalculate:
            m = networkx.closeness_centrality(g)
            l = sorted(m.items(), key=operator.itemgetter(1), 
                       reverse=True)
        largest_component = max(networkx.connected_components(g), key=len)
        x.append(i * 1. / n)
        r += len(largest_component) * 1. / n
        y.append(len(largest_component) * 1. / n)
    return x, y, r / n


def closeness_apl(g, recalculate=False):
    """
    Performs robustness analysis based on closeness centrality,
    on the network specified by infile using sequential (recalculate = True)
    or simultaneous (recalculate = False) approach. Returns a list
    with fraction of nodes removed, a list with the corresponding sizes of
    the largest component of the network, and the overall vulnerability
    of the network.
    """

    m = networkx.closeness_centrality(g)
    l = sorted(m.items(), key=operator.itemgetter(1), reverse=True)
    x = []
    y = []

    average_path_length = 0.0
    number_of_components = 0
    n = len(g.nodes())

    for sg in networkx.connected_component_subgraphs(g):
        average_path_length += networkx.average_shortest_path_length(sg)
        number_of_components += 1

    average_path_length = average_path_length / number_of_components
    initial_apl = average_path_length

    x.append(0)
    y.append(average_path_length * 1. / initial_apl)

    r = 0.0
    for i in range(1, n):
        g.remove_node(l.pop(0)[0])
        if recalculate:
            m = networkx.closeness_centrality(g)
            l = sorted(m.items(), key=operator.itemgetter(1),
                       reverse=True)

        average_path_length = 0.0
        number_of_components = 0

        for sg in networkx.connected_component_subgraphs(g):
            if len(sg.nodes()) > 1:
                average_path_length += networkx.average_shortest_path_length(sg)
            number_of_components += 1

        average_path_length = average_path_length / number_of_components

        x.append(i * 1. / initial_apl)
        r += average_path_length * 1. / initial_apl
        y.append(average_path_length * 1. / initial_apl)
    return x, y, r / initial_apl


def degree(g, recalculate=False):
    """
    Performs robustness analysis based on degree centrality,  
    on the network specified by infile using sequential (recalculate = True) 
    or simultaneous (recalculate = False) approach. Returns a list 
    with fraction of nodes removed, a list with the corresponding sizes of 
    the largest component of the network, and the overall vulnerability 
    of the network.
    """

    m = networkx.degree_centrality(g)
    l = sorted(m.items(), key=operator.itemgetter(1), reverse=True)
    x = []
    y = []
    largest_component = max(networkx.connected_components(g), key=len)
    n = len(g.nodes())
    x.append(0)
    y.append(len(largest_component) * 1. / n)
    r = 0.0
    for i in range(1, n - 1):
        g.remove_node(l.pop(0)[0])
        if recalculate:
            m = networkx.degree_centrality(g)
            l = sorted(m.items(), key=operator.itemgetter(1), 
                       reverse=True)
        largest_component = max(networkx.connected_components(g), key=len)
        x.append(i * 1. / n)
        r += len(largest_component) * 1. / n
        y.append(len(largest_component) * 1. / n)
    return x, y, r / n


def degree_apl(g, recalculate=False):
    """
    Performs robustness analysis based on degree centrality,
    on the network specified by infile using sequential (recalculate = True)
    or simultaneous (recalculate = False) approach. Returns a list
    with fraction of nodes removed, a list with the corresponding sizes of
    the largest component of the network, and the overall vulnerability
    of the network.
    """

    m = networkx.degree_centrality(g)
    l = sorted(m.items(), key=operator.itemgetter(1), reverse=True)
    x = []
    y = []

    average_path_length = 0.0
    number_of_components = 0
    n = len(g.nodes())

    for sg in networkx.connected_component_subgraphs(g):
        average_path_length += networkx.average_shortest_path_length(sg)
        number_of_components += 1

    average_path_length = average_path_length / number_of_components
    initial_apl = average_path_length

    x.append(0)
    y.append(average_path_length * 1. / initial_apl)

    r = 0.0
    for i in range(1, n - 2):
        g.remove_node(l.pop(0)[0])
        if recalculate:
            m = networkx.degree_centrality(g)
            l = sorted(m.items(), key=operator.itemgetter(1),
                       reverse=True)

        average_path_length = 0.0
        number_of_components = 0

        for sg in networkx.connected_component_subgraphs(g):
            if len(sg.nodes()) > 1:
                average_path_length += networkx.average_shortest_path_length(sg)
            number_of_components += 1


        average_path_length = average_path_length / number_of_components

        x.append(i * 1. / initial_apl)
        r += average_path_length * 1. / initial_apl
        y.append(average_path_length * 1. / initial_apl)
    return x, y, r / initial_apl


def eigenvector(g, recalculate=False):
    """
    Performs robustness analysis based on eigenvector centrality,  
    on the network specified by infile using sequential (recalculate = True) 
    or simultaneous (recalculate = False) approach. Returns a list 
    with fraction of nodes removed, a list with the corresponding sizes of 
    the largest component of the network, and the overall vulnerability 
    of the network.
    """

    m = networkx.eigenvector_centrality(g, max_iter=5000)
    l = sorted(m.items(), key=operator.itemgetter(1), reverse=True)
    x = []
    y = []
    largest_component = max(networkx.connected_components(g), key=len)
    n = len(g.nodes())
    x.append(0)
    y.append(len(largest_component) * 1. / n)
    r = 0.0
    for i in range(1, n - 1):
        g.remove_node(l.pop(0)[0])
        if recalculate:

            try:
                m = networkx.eigenvector_centrality(g, max_iter=5000)
            except networkx.NetworkXError:
                break

            l = sorted(m.items(), key=operator.itemgetter(1),
                       reverse=True)
        largest_component = max(networkx.connected_components(g), key=len)
        x.append(i * 1. / n)
        r += len(largest_component) * 1. / n
        y.append(len(largest_component) * 1. / n)
    return x, y, r / n


def eigenvector_apl(g, recalculate=False):
    """
    Performs robustness analysis based on eigenvector centrality,
    on the network specified by infile using sequential (recalculate = True)
    or simultaneous (recalculate = False) approach. Returns a list
    with fraction of nodes removed, a list with the corresponding sizes of
    the largest component of the network, and the overall vulnerability
    of the network.
    """

    m = networkx.eigenvector_centrality(g)
    l = sorted(m.items(), key=operator.itemgetter(1), reverse=True)
    x = []
    y = []

    average_path_length = 0.0
    number_of_components = 0
    n = len(g.nodes())

    for sg in networkx.connected_component_subgraphs(g):
        average_path_length += networkx.average_shortest_path_length(sg)
    number_of_components += 1

    average_path_length /= number_of_components
    initial_apl = average_path_length

    r = 0.0
    for i in range(1, n - 1):
        g.remove_node(l.pop(0)[0])
        if recalculate:

            try:
                m = networkx.eigenvector_centrality(g, max_iter=5000)
            except networkx.NetworkXError:
                break

            l = sorted(m.items(), key=operator.itemgetter(1),
                       reverse=True)
        average_path_length = 0.0
        number_of_components = 0

        for sg in networkx.connected_component_subgraphs(g):
            if len(sg.nodes()) > 1:
                average_path_length += networkx.average_shortest_path_length(sg)
            number_of_components += 1

        average_path_length = average_path_length / number_of_components

        x.append(i * 1. / initial_apl)
        r += average_path_length * 1. / initial_apl
        y.append(average_path_length * 1. / initial_apl)
    return x, y, r / initial_apl


def rand(g):
    """
    Performs robustness analysis based on random attack, on the network 
    specified by infile. Returns a list with fraction of nodes removed, a 
    list with the corresponding sizes of the largest component of the 
    network, and the overall vulnerability of the network.
    """

    l = [(node, 0) for node in g.nodes()]
    random.shuffle(l)
    x = []
    y = []
    largest_component = max(networkx.connected_components(g), key=len)
    n = len(g.nodes())
    x.append(0)
    y.append(len(largest_component) * 1. / n)
    r = 0.0
    for i in range(1, n):
        g.remove_node(l.pop(0)[0])
        largest_component = max(networkx.connected_components(g), key=len)
        x.append(i * 1. / n)
        r += len(largest_component) * 1. / n
        y.append(len(largest_component) * 1. / n)
    return x, y, r / n


def rand_apl(g):
    """
    Performs robustness analysis based on random attack, on the network
    specified by infile. Returns a list with fraction of nodes removed, a
    list with the corresponding sizes of the largest component of the
    network, and the overall vulnerability of the network.
    """

    l = [(node, 0) for node in g.nodes()]
    random.shuffle(l)
    x = []
    y = []

    average_path_length = 0.0
    number_of_components = 0
    n = len(g.nodes())

    for sg in networkx.connected_component_subgraphs(g):
        average_path_length += networkx.average_shortest_path_length(sg)
        number_of_components += 1

    average_path_length = average_path_length / number_of_components
    initial_apl = average_path_length

    r = 0.0
    for i in range(1, n):
        g.remove_node(l.pop(0)[0])

        average_path_length = 0.0
        number_of_components = 0

        for sg in networkx.connected_component_subgraphs(g):
            if len(sg.nodes()) > 1:
                average_path_length += networkx.average_shortest_path_length(sg)
            number_of_components += 1

        average_path_length = average_path_length / number_of_components

        x.append(i * 1. / initial_apl)
        r += average_path_length * 1. / initial_apl
        y.append(average_path_length * 1. / initial_apl)
    return x, y, r / initial_apl


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
    else:
        apl = False

    if argv[3] == "True":
        recalculate = True
    else:
        recalculate = False

    if not apl:
        g = networkx.read_gml(infile).to_undirected()
        x1, y1, vd = degree(g.copy(), recalculate)
        x2, y2, vb = betweenness(g.copy(), recalculate)
        x3, y3, vc = closeness(g.copy(), recalculate)
        x4, y4, VE = eigenvector(g.copy(), recalculate)
        x5, y5, vr = rand(g.copy())

        pylab.figure(1, dpi=500)
        pylab.xlabel(r"Fraction of vertices removed ($\rho$)")
        pylab.ylabel(r"Fractional size of largest component ($\sigma$)")
    else:
        g = networkx.read_gml(infile).to_undirected()
        x1, y1, vd = degree_apl(g.copy(), recalculate)
        x2, y2, vb = betweenness_apl(g.copy(), recalculate)
        x3, y3, vc = closeness_apl(g.copy(), recalculate)
        x4, y4, VE = eigenvector_apl(g.copy(), recalculate)
        x5, y5, vr = rand_apl(g.copy())

        pylab.figure(1, dpi=500)
        pylab.xlabel(r"Fraction of vertices removed ($\rho$)")
        pylab.ylabel(r"Average path length ($\sigma$)")

    pylab.plot(x1, y1, "b-", alpha=0.6, linewidth=2.0)
    pylab.plot(x2, y2, "g-", alpha=0.6, linewidth=2.0)
    pylab.plot(x3, y3, "r-", alpha=0.6, linewidth=2.0)
    pylab.plot(x4, y4, "c-", alpha=0.6, linewidth=2.0)
    pylab.plot(x5, y5, "k-", alpha=0.6, linewidth=2.0)

    if not apl:
        pylab.legend((r"Degree ($R = %4.3f$)" % vd,
                      "Betweenness ($R = %4.3f$)" % vb,
                      "Closeness ($R = %4.3f$)" % vc,
                      "Eigenvector ($R = %4.3f$)" % VE,
                      "Random ($R = %4.3f$)" % vr),
                      loc="upper right", shadow=False)
    else:
        pylab.legend((r"Degree ($R = %4.3f$)" % vd,
                      "Betweenness ($R = %4.3f$)" % vb,
                      "Closeness ($R = %4.3f$)" % vc,
                      "Eigenvector ($R = %4.3f$)" % VE,
                      "Random ($R = %4.3f$)" % vr),
                       loc="upper right", shadow=False,
                       bbox_to_anchor=(1.12, 1.09))



    pylab.savefig(outfile, format="png")
    pylab.close(1)

if __name__ == "__main__":
    main(sys.argv[1:])
