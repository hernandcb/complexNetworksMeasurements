#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:57:25 2015
@author: Hernán David Carvajal Bastidas

Module to test an algorithm with random networks.

"""

import networkx as nx
from random import seed, randint

def randomNum():
	return randint(1, 10000)

def generateRandomNetworks(_seed=622527):
	seed(_seed)
	# Network size will be 10^1, 10 ^2, 10^3, 10^4
	for exponent in range(1, 5): # 1 .. 4
		networkSize = 10 ** exponent
		
		for probability in [0.1, 0.3, 0.5, 0.7, 0.9]:
			print(randomNum())
			# Generate erdos Renyi networks
			# nx.erdos_renyi_graph(networkSize, probability, seed)
			
