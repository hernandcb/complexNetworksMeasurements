#
#Code in Python (written by Hernan Carvajal):
# 
#For this code to run you'll need to install Python (http://www.python.org)
#and Networkx (http://networkx.lanl.gov/).
# 
#File "fractalDimension.py" 
#
#Calculate the fractal dimension of a network by using the box covering algorithm

from .boxCovering.greedyColoring import *
import random as rnd
import numpy as np
import time
 

def calculateFractalDimension(graph, lb_max, iterations=10000, seed=3786689, print_results=False, print_dir=""): 

	# Give a default name to the graph ('network') in case it's not defined
	graphName = graph.graph.get("name", "network") + "_results"
	date = time.strftime("%Y-%m-%d_%H%M%S")
	resultsFileName = graphName + "_" + date
	
	file = open('out.txt', 'w')
	rnd.seed(seed)
	n = len(graph.nodes())
	
	# Create a dictionary of lists to store all the number 
	# of boxes obtained for each box length
	results = {k: [] for k in range(1, lb_max+1)}	
	
	# Calculate the number of nodes for each box length - {iterations} times
	for i in range(iterations): # 2 .. lb_max -13
		boxes = greedyColoring(graph, True, rnd.randint(1, 9999))
		if print_results:
			file = open("{}_{}.out".format(resultsFileName, rnd.randint(1, 9999)) , 'w')
			
		for lb in range(1, lb_max+1): # 2 .. lb_max
			results[lb].append( len(boxes[lb -1]) )
			if print_results:
				file.write("{} {}\n".format(lb, len(boxes[lb -1])) )
		
		if print_results:
			file.close()

	box_length = []
	mean_nodes_per_box = []

	# Calculate the average number of nodes for each box length
	for lb in range (1, lb_max + 1):
		box_length.append(lb)
		nodes_per_box = np.array(results[lb])
		
		mean_nodes_per_box.append( np.mean(nodes_per_box) )
	
	
	# Fit a line and calculate the slope
	log_box_length = np.log(np.array(box_length))
	log_mean_number_of_nodes = np.log(np.array(mean_nodes_per_box))

	slope, intercept = np.polyfit( log_box_length, log_mean_number_of_nodes, 1)
	
	return slope  # The slope of the line is the fractal dimension