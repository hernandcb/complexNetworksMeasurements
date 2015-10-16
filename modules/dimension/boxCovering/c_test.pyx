#!/usr/bin/python
# Author: Hernán David Carvajal <carvajal.hernandavid at gmail.com>
# Tested in python-3.4.3
import numpy as np

cimport cython
cimport numpy as np
from libc.stdlib cimport malloc, free, rand

DTYPE = np.int
ctypedef np.int_t DTYPE_t


cdef choose_color(set not_valid_colors, set valid_colors):
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
    cdef int  i, lb, j,
    cdef np.ndarray[DTYPE_t, ndim=2] c = np.empty((num_nodes+1, diameter+2), dtype=DTYPE)

    cdef int *nodes
    nodes = <int *>malloc(num_nodes * cython.sizeof(int))

    cdef set valid_colors, not_valid_colors

    if nodes is NULL:
        raise MemoryError()

    c.fill(-1)

    # nodes = list(range(1, num_nodes+1))
    for i from 0 <= i < num_nodes:
        nodes[i] = i+1

    shuffle(nodes, num_nodes)

    for i from 0 <= i <= diameter:
        c[nodes[0], i] = 0

    # Algorithm
    for index from 1 <= index < num_nodes:
        i = nodes[index]
        for lb from 2 <= lb <= diameter:
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


def test():
    cdef np.ndarray[DTYPE_t, ndim=2] distances = np.matrix('0 3 2 4 1 1; \
                           3 0 1 1 3 2; \
                           2 1 0 2 2 1; \
                           4 1 2 0 4 3; \
                           1 3 2 4 0 1; \
                           1 2 1 3 1 0')

    cdef np.ndarray[DTYPE_t, ndim=2] c = greedy_coloring(distances, 6, 4)
    # print(c)
