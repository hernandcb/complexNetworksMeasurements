# -*- coding: utf-8 -*-
"""

This script reads the network information from a given file and 
store it into the database.

@author Hernán David Carvajal
"""

import database.databaseManager as db
import networkx as nx, os

network = None

def save_network_info(networkFile, networkName="", networkDescription=""):
	"""
	Read a network from a graph6 file stored in the data folder of the 
	project and save its basic information to the database.
	
	TODO - generalize this method to work with any file type allowed by the
	library
	"""
	
	network = nx.read_graph6(networkFile)
	if nx.is_directed(network):
		network = network.to_undirected()
	
	filename = os.path.basename(networkFile)
	name = filename.replace('.', '_') if networkName is "" else networkName
	
	# If the newtork is not connected the diameter would be stored as 0
	diameter =  nx.diameter(network) if nx.is_connected(network) else 0
	
	db.connect()
	query = ("INSERT INTO networks (name, description, filename, "
               "number_of_nodes, diameter) VALUES (%s, %s, %s, %s, %s) ")
	
	data = (name, networkDescription, filename, network.number_of_nodes(), diameter)
	db.connect()
	db.makeChange(query, data)
	db.disconnect()
	

def store_network_distances(networkName):
	None

def load_network(networkName):
	global network
	
	if network is None:
		query = ("SELECT * FROM networks WHERE name = {}".format(name))
		print(query)
	
if __name__ == "__main__":
    load_network("randomNetworks/barabasi_albert_n10_m1.graph6")
	