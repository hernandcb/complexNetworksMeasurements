import sys
import random
import networkit as nk
import dimension.fractalDimension as fd

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


def test(g):

    nodes = g.nodes()
    random.shuffle(nodes)
    x = []
    y = []

    dimension = fd.fractal_dimension(g, iterations=100, debug=False)
    n = len(nodes)

    x.append(0)
    y.append(dimension)
    r = 0.0

    for i in range(1, n-1):
        remove_node(g, nodes.pop(0))
        print(i)
        dimension = fd.fractal_dimension(g, iterations=100, debug=False)

        x.append(i * 1. / n)
        y.append(dimension)

    print(x, y)
    # return x, y


if __name__ == "__main__":
    infile = sys.argv[1]

    print(infile)
    g = nk.readGraph(infile, nk.Format.GML)
    test(g)
