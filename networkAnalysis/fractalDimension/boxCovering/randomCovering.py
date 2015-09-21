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
import fractal_model as fm

def random_box_covering(G,rb):
	"""
	It returns a dictionary with {box_id:subgraph_generated_by_the_nodes_in_this_box}
	The box_id is the center of the box.
	"""
	H = deepcopy(G)
	burned_nodes = []
	unburned_nodes = G.nodes()
	boxes_subgraphs = {}
	adj = H.adj
	while unburned_nodes:
		center_node = random.choice(unburned_nodes) 
		nodes_visited = [center_node]
		search_queue = [center_node]
		d = 1
		while search_queue and d <= rb:
			next_depth = []
			extend = next_depth.extend
			for n in search_queue:
				l = [ i for i in iter(adj[n].keys()) if i not in nodes_visited]
				extend(l)
				nodes_visited.extend(l)
			search_queue = next_depth
			d += 1
		new_burned_nodes = nodes_visited#.keys()
		H.delete_nodes_from(new_burned_nodes)
		boxes_subgraphs[center_node] = subgraph(G,new_burned_nodes)
		unburned_nodes = list(set(unburned_nodes)-set(new_burned_nodes))
	return boxes_subgraphs

""""
if __name__ == '__main__':
	g=fm.fractal_model(3,2,2,0)
	boxes_subgraphs = MEMB(g,2)
	print boxes_subgraphs
"""
