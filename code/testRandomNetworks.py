# -*- coding: utf-8 -*-
import fractalDimension.fractalDimension as fd
import random as rnd
import networkx as nx
import glob
import os

randomNetworksFolder = "../data/randomNetworks/"
#randomNetworksFolder = "../data/realNetworks/Dolphin social network/" 

def testFractalDimension(resultsFolder="", seed=837172):
	rnd.seed(seed)
	networksList = getGraph6Files(randomNetworksFolder)
	
	for network in networksList:
		# Load the network
		dgraph = nx.read_graph6(network) 
		graph = dgraph.to_undirected()
		graph.graph["name"] = os.path.basename(network).replace('.', '_')
		print(graph.graph["name"])

		max_box_size = nx.diameter(graph) + 1

		for i in range(80):
			n = rnd.randint(1, 999999)
			dimension = fd.calculateFractalDimension(graph, max_box_size, seed=n)
			file = open("{}{}.out".format(resultsFolder, graph.graph["name"]) , 'w')
			file.write("{}\n".format(dimension))
			file.close()
	
	
	
# return all .graph6 files contained in directory
def getGraph6Files(directory):
	# The list is returned with inverse order to start with the small files first
	return sorted(glob.glob(directory + "*.graph6"), reverse=True)
	
if __name__ == '__main__':
	testFractalDimension("")