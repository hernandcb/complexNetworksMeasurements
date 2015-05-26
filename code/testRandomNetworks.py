# -*- coding: utf-8 -*-
import fractalDimension.fractalDimension as fd
import random as rnd
import networkx as nx
import glob
import os

#randomNetworksFolder = "../data/randomNetworks/"
randomNetworksFolder = "../data/realNetworks/Dolphin social network/" 

def testFractalDimension(seed=837172):
	rnd.seed(seed)
	networksList = getGraph6Files(randomNetworksFolder)
	
	for network in networksList:
		# Load the network
		dgraph = nx.read_gml(network) 
		graph = dgraph.to_undirected()
		
		graph.graph["name"] = os.path.basename(network).replace('.', '_')

		max_box_size = nx.diameter(graph) + 1

		for i in range(80):
			n = rnd.randint(1, 999999)
			dimension = fd.calculateFractalDimension(graph, max_box_size, iterations=5, seed=n, print_results=True)		
			print(dimension)
	
	
# return all .graph6 files contained in directory
def getGraph6Files(directory):
	return glob.glob(directory + "*.gml")
	
if __name__ == '__main__':
	testFractalDimension()