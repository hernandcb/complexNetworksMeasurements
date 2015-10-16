import random as rnd
import numpy as np


def choose_color(not_valid_colors, valid_colors):
    possible_values = list(valid_colors - not_valid_colors)

    if possible_values:
        return rnd.choice(possible_values)
    else:
        return max(valid_colors.union(not_valid_colors)) + 1


def greedy_coloring(distances, num_nodes, diameter):

    c = np.empty((num_nodes+1, diameter+2), dtype=int)
    c.fill(-1)
    # Matrix C will not use the 0 column and 0 row to
    # let the algorithm look very similar to the paper
    # pseudo-code

    nodes = list(range(1, num_nodes+1))
    rnd.shuffle(nodes)

    for j in range(diameter+1):
        c[nodes[0]][j] = 0

    # Algorithm
    for i in nodes[1:]:
        for lb in range(1, diameter+2):
            not_valid_colors = set()
            valid_colors = set()

            for j in nodes:
                if j == i:
                    break

                if distances[i-1, j-1] >= lb:
                    not_valid_colors.add(c[j][lb])
                else:
                    valid_colors.add(c[j][lb])

            c[i][lb] = choose_color(not_valid_colors, valid_colors)

    return c


def test():
    distances = np.matrix('0 3 2 4 1 1; \
                           3 0 1 1 3 2; \
                           2 1 0 2 2 1; \
                           4 1 2 0 4 3; \
                           1 3 2 4 0 1; \
                           1 2 1 3 1 0')

    c = greedy_coloring(distances, 6, 4)
    # print(c)


if __name__ == "__main__":
    test()
