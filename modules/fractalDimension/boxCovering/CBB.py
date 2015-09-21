#Comments:
#
#If you have any questions or find a bug write Hernan Rozenfeld an email at
#hernanrozenfeld at domain gmail with the usual "dot com" at the end.
# 
#Code in Python (written by Hernan Rozenfeld):
# 
#For this code to run you'll need to install Python (http://www.python.org)
#and Networkx (http://networkx.lanl.gov/).
# 
#File "modules.py" contains algorithms MEMB, CBB, and random covering for
#network renormalization.


import numpy as np
import networkx as nx
import random
from copy import deepcopy
import os, sys
import time
import fractalModel as fm


def CBB(G,lb): #This is the compact box burning algorithm.
	"""
	It returns a dictionary with {box_id:subgraph_generated_by_the_nodes_in_this_box}
	The box_id is the center of the box.
	The subgraphs may be disconnected.
	"""	
	uncovered_nodes=G.nodes()
	uncovered_nodes = set(uncovered_nodes)
	covered_nodes = set([])
	boxes_subgraphs = {}
	adj = G.adj
	while uncovered_nodes:
		center = random.choice(list(uncovered_nodes))
		nodes_visited = {center:0}
		search_queue = [center]
		d = 1
		while len(search_queue) > 0 and d <= lb-1:
			next_depth = []
			extend = next_depth.extend
			for n in search_queue:
				l = [ i for i in iter(adj[n].keys()) if i not in nodes_visited ]
				extend(l)
				for j in l: 
					nodes_visited[j] = d
			search_queue = next_depth
			d += 1
		new_covered_nodes = set(nodes_visited.keys())
		new_covered_nodes = new_covered_nodes.difference(covered_nodes)
		nodes_checked_as_centers = set([center])
		while len(nodes_checked_as_centers) < len(new_covered_nodes):
			secondary_center = random.choice(list(new_covered_nodes.difference(nodes_checked_as_centers)))
			nodes_checked_as_centers.add(secondary_center)
			nodes_visited = {secondary_center:0}
			search_queue = [secondary_center]
			d = 1
			while len(search_queue) > 0 and d <= lb-1:
				next_depth = []
				extend = next_depth.extend
				for n in search_queue:
					l = [ i for i in iter(adj[n].keys()) if i not in nodes_visited ] # faster than has_key? yep
					extend(l)
					for j in l:
						nodes_visited[j] = d
				search_queue = next_depth
				d += 1
			nodes_covered_by_secondary = set(nodes_visited.keys())
			new_covered_nodes = new_covered_nodes.intersection(nodes_covered_by_secondary)
		boxes_subgraphs[center] = nx.subgraph(G,list(new_covered_nodes))
		uncovered_nodes = uncovered_nodes.difference(new_covered_nodes)
		covered_nodes = covered_nodes.union(new_covered_nodes)
	return boxes_subgraphs

""""
if __name__ == '__main__':
	g=fm.fractal_model(3,2,2,0)
	boxes_subgraphs = CBB(g,2)
	print(boxes_subgraphs)
""""
