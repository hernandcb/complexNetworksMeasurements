#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:57:25 2015
@author: Hernán David Carvajal Bastidas

Module to test an algorithm with random networks.

"""

import networkx as nx
from random import seed, randint

directory = "../data/randomNetworks/"

def randomNum():
	return randint(1, 10000)

def generateRandomNetworks(randomSeed=622527):
	seed(randomSeed)
	# Network size will be 10^1, 10 ^2, 10^3, 10^4
	for exponent in range(1, 4): # 1 .. 4
		n = 10 ** exponent

		for p in [0.1, 0.3, 0.5, 0.7, 0.9]:
			m = round(n * p)

			# Generate erdos Renyi networks
			graph = nx.erdos_renyi_graph(n, p, randomNum())
			graphName = "erdos_renyi_n{}_p{}.graph6".format(n, p)
			nx.write_graph6(graph, directory + graphName)
			
			# Generate Barabasi Albert networks
			graph = nx.barabasi_albert_graph(n, m, randomNum())
			graphName = "barabasi_albert_n{}_m{}.graph6".format(n, m)
			nx.write_graph6(graph, directory + graphName)
			
			for k in [0.1, 0.3, 0.5, 0.7, 0.9]:
				k = round(n * k)
				# Generate Watts Strogatz networks
				graph = nx.watts_strogatz_graph(n, k, p, randomNum())
				graphName = "watts_strogatz_n{}_k{}_p{}.graph6".format(n, k, p)
				nx.write_graph6(graph, directory + graphName)
	
			

generateRandomNetworks()